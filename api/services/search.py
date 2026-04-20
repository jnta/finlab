from qdrant_client import QdrantClient, models
from api.models.search import SearchResponse, SearchResult
from api.services.embeddings import EmbeddingsService


class SearchService:
    def __init__(self, qdrant_url: str, qdrant_api_key: str, collection_name: str):
        self.qdrant = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        self.collection_name = collection_name
        self.embeddings_service = EmbeddingsService()

    def search(self, query: str, limit: int = 3) -> SearchResponse:
        dense, sparse, colbert = self.embeddings_service.embed_query(query)
        results = self.qdrant.query_points(
            collection_name=self.collection_name,
            prefetch=[
                {
                    "prefetch": [
                        {"query": dense, "using": "dense", "limit": 20},
                        {"query": sparse, "using": "sparse_vector", "limit": 20},
                    ],
                    "query": models.FusionQuery(fusion=models.Fusion.RRF),
                    "limit": 15,
                }
            ],
            query=colbert,
            using="colbert",
            limit=limit,
        )

        if not results or not results.points:
            return SearchResponse(results=[])

        max_score = max(result.score for result in results.points)
        search_results = [
            SearchResult(
                score=result.score / max_score if max_score > 0 else 0,
                text=result.payload["text"],
                metadata=result.payload["metadata"],
            )
            for result in results.points
        ]
        return SearchResponse(results=search_results)
