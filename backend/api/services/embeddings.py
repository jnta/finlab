from fastembed import TextEmbedding, SparseTextEmbedding, LateInteractionTextEmbedding
from api.config.settings import settings


class EmbeddingsService:
    def __init__(self):
        import os
        cache_dir = os.path.abspath("./.fastembed_cache")
        self.dense_model = TextEmbedding(
            model_name=settings.dense_model, cache_dir=cache_dir
        )
        self.sparse_model = SparseTextEmbedding(
            model_name=settings.sparse_model, cache_dir=cache_dir
        )
        self.colbert_model = LateInteractionTextEmbedding(
            model_name=settings.colbert_model, cache_dir=cache_dir
        )

    def embed_query(self, query: str):
        dense = list(self.dense_model.query_embed([query]))[0].tolist()
        sparse = list(self.sparse_model.query_embed([query]))[0].as_object()
        colbert = list(self.colbert_model.query_embed([query]))[0].tolist()

        return dense, sparse, colbert
