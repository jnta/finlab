from fastapi import APIRouter, HTTPException
from api.config.settings import settings
from api.services.search import SearchService
from api.services.agent import AgentService
from api.models.agent import AgentRequest, AgentResponse

router = APIRouter(prefix="/agent", tags=["agent"])

search_service = SearchService(
    qdrant_url=settings.qdrant_url,
    qdrant_api_key=settings.qdrant_api_key,
    collection_name=settings.collection_name,
)

agent_service = AgentService(search_service=search_service)


@router.post("/analyze", response_model=AgentResponse)
async def analyze(request: AgentRequest):
    try:
        return await agent_service.analyze(request.query, request.limit)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
