import uuid
from fastapi import HTTPException, status
from qdrant_client import QdrantClient, models

from api.config.settings import settings
from api.services.embeddings import EmbeddingsService

from api.clients.edgar_client import EdgarClient
from api.clients.news_client import NewsClient
from api.utils.semantic_chunker import SemanticChunker
from api.utils.simple_chunker import SimpleChunker


class IngestService:
    def __init__(self, qdrant_url: str, qdrant_api_key: str, collection_name: str):
        self.qdrant = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        self.collection_name = collection_name
        self.embeddings_service = EmbeddingsService()
        self.edgar_client = EdgarClient(settings.edgar_email)
        self.news_client = NewsClient()
        self.chunker = SemanticChunker(
            embed_model=self.embeddings_service.dense_model, max_tokens=300
        )
        self.simple_chunker = SimpleChunker()

    def ingest_ticker(self, ticker: str) -> str:
        try:
            count_result = self.qdrant.count(
                collection_name=self.collection_name,
                count_filter=models.Filter(
                    should=[
                        models.FieldCondition(
                            key="metadata.ticker", match=models.MatchValue(value=ticker)
                        ),
                        models.FieldCondition(
                            key="metadata.symbol", match=models.MatchValue(value=ticker)
                        ),
                        models.FieldCondition(
                            key="ticker", match=models.MatchValue(value=ticker)
                        ),
                    ]
                ),
                exact=True,
            )
            if count_result.count > 0:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ingestion for {ticker} already exists.",
                )
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            pass

        data_10k = self.edgar_client.fetch_filing_data(ticker, "10-K")
        data_10q = self.edgar_client.fetch_filing_data(ticker, "10-Q")

        content_10k = self.edgar_client.get_combined_text(data_10k)
        content_10q = self.edgar_client.get_combined_text(data_10q)

        all_chunks = []
        for data, text in [(data_10k, content_10k), (data_10q, content_10q)]:
            chunks = self.chunker.create_chunks(text)
            for chunk in chunks:
                all_chunks.append({"text": chunk, "metadata": data.get("metadata", {})})

        points = []
        for chunk_data in all_chunks:
            chunk = chunk_data["text"]
            metadata = chunk_data["metadata"]

            if "ticker" not in metadata and "symbol" not in metadata:
                metadata["ticker"] = ticker

            dense_emb = list(
                self.embeddings_service.dense_model.passage_embed([chunk])
            )[0].tolist()
            sparse_emb = list(
                self.embeddings_service.sparse_model.passage_embed([chunk])
            )[0].as_object()
            colbert_emb = list(
                self.embeddings_service.colbert_model.passage_embed([chunk])
            )[0].tolist()

            point = models.PointStruct(
                id=str(uuid.uuid4()),
                vector={
                    "dense": dense_emb,
                    "sparse_vector": sparse_emb,
                    "colbert": colbert_emb,
                },
                payload={"text": chunk, "metadata": metadata},
            )
            points.append(point)

        if points:
            self.qdrant.upload_points(
                collection_name=self.collection_name, points=points, batch_size=5
            )

        return f"Ingestion completed successfully for {ticker}!"

    def ingest_news(self, ticker: str, max_stories: int = 10) -> str:
        news_data = self.news_client.fetch_news(ticker, max_stories)
        if not news_data:
            return f"No news found for {ticker}."

        all_chunks = []
        for item in news_data:
            text = item["text"]
            metadata = item["metadata"]
            chunks = self.simple_chunker.create_chunks(text)
            for chunk in chunks:
                all_chunks.append({"text": chunk, "metadata": metadata})

        points = []
        for chunk_data in all_chunks:
            chunk = chunk_data["text"]
            metadata = chunk_data["metadata"]

            dense_emb = list(
                self.embeddings_service.dense_model.passage_embed([chunk])
            )[0].tolist()
            sparse_emb = list(
                self.embeddings_service.sparse_model.passage_embed([chunk])
            )[0].as_object()
            colbert_emb = list(
                self.embeddings_service.colbert_model.passage_embed([chunk])
            )[0].tolist()

            point = models.PointStruct(
                id=str(uuid.uuid4()),
                vector={
                    "dense": dense_emb,
                    "sparse_vector": sparse_emb,
                    "colbert": colbert_emb,
                },
                payload={"text": chunk, "metadata": metadata},
            )
            points.append(point)

        if points:
            self.qdrant.upload_points(
                collection_name=self.collection_name, points=points, batch_size=5
            )

        return f"News ingestion completed successfully for {ticker}!"
