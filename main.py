from fastapi import FastAPI
from api.models.search import SearchRequest, SearchResponse
from api.services.search import SearchService
from api.config.settings import settings

app = FastAPI(title="Financial Search API")
search_service = SearchService(
    qdrant_url=settings.qdrant_url,
    qdrant_api_key=settings.qdrant_api_key,
    collection_name=settings.collection_name,
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/search", response_model=SearchResponse)
def search(request: SearchRequest):
    return search_service.search(request.query, request.limit)
