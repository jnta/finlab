from fastapi import APIRouter
from api.config.settings import settings
from api.services.ingest import IngestService
from api.models.ingest import IngestRequest, IngestResponse

router = APIRouter()

ingest_service = IngestService(
    qdrant_url=settings.qdrant_url,
    qdrant_api_key=settings.qdrant_api_key,
    collection_name=settings.collection_name,
)

@router.post("/ingest", response_model=IngestResponse)
def ingest(request: IngestRequest):
    message = ingest_service.ingest(request.ticker)
    return IngestResponse(message=message)
