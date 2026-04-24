from typing import Optional, Dict, Any
from qdrant_client import QdrantClient, models
from api.models.search import SearchResponse, SearchResult
from api.services.embeddings import EmbeddingsService


class SearchService:
    def __init__(self, qdrant_url: str, qdrant_api_key: str, collection_name: str):
        self.qdrant = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        self.collection_name = collection_name
        self.embeddings_service = EmbeddingsService()

    def _build_filter_clauses(self, filters: Optional[Dict[str, Any]] = None):
        if not filters:
            return None

        must_conditions = []

        for key, value in filters.items():
            must_conditions.append(
                {
                    "key": f"metadata.{key}",
                    "match": {"value": value},
                }
            )
        return {"must": must_conditions}

    def search(
        self, query: str, limit: int = 3, filters: Optional[Dict[str, Any]] = None
    ) -> SearchResponse:
        filter_clauses = self._build_filter_clauses(filters)

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
            query_filter=filter_clauses,
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
