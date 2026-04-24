from fastapi import APIRouter
from api.config.settings import settings
from api.services.ingest import IngestService
from api.models.ticker_ingest import TickerIngestRequest, IngestResponse
from api.models.news_ingest import NewsIngestRequest

router = APIRouter(prefix="/ingest", tags=["ingest"])

ingest_service = IngestService(
    qdrant_url=settings.qdrant_url,
    qdrant_api_key=settings.qdrant_api_key,
    collection_name=settings.collection_name,
)

@router.post("/ticker", response_model=IngestResponse)
def ingest_ticker(request: TickerIngestRequest):
    message = ingest_service.ingest_ticker(request.ticker)
    return IngestResponse(message=message)

@router.post("/news", response_model=IngestResponse)
def ingest_news(request: NewsIngestRequest):
    message = ingest_service.ingest_news(request.ticker, request.max_stories)
    return IngestResponse(message=message)
