import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from api.services.agent import AgentService
from api.models.agent import AgentResponse
from api.models.search import SearchResponse, SearchResult

@pytest.fixture
def mock_search_service():
    service = MagicMock()
    service.search.return_value = SearchResponse(results=[
        SearchResult(score=1.0, text="Mocked context", metadata={})
    ])
    return service

@pytest.fixture
def agent_service(mock_search_service):
    with patch("api.services.agent.settings") as mock_settings:
        mock_settings.groq_api_key = "fake_key"
        mock_settings.groq_model = "fake_model"
        return AgentService(search_service=mock_search_service)

@pytest.mark.asyncio
async def test_analyze_orchestration(agent_service):
    # Mock groq client
    agent_service.groq_client = AsyncMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Mocked LLM Response"
    agent_service.groq_client.chat.completions.create.return_value = mock_response

    response = await agent_service.analyze(ticker="AAPL", limit=1)

    assert isinstance(response, AgentResponse)
    assert response.ticker == "AAPL"
    
    # Verify search service was called for fundamental, momentum, and sentiment
    # Fundamental queries: multiple calls in _run_queries loop
    # Momentum queries: multiple calls
    # Sentiment query: 1 call
    # Total calls depend on the number of queries in the config.
    assert agent_service.search_service.search.called

    # Verify LLM was called 4 times (3 analysis + 1 aggregation)
    assert agent_service.groq_client.chat.completions.create.call_count == 4

@pytest.mark.asyncio
async def test_generate_completion(agent_service):
    agent_service.groq_client = AsyncMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "LLM says hello"
    agent_service.groq_client.chat.completions.create.return_value = mock_response

    result = await agent_service._generate_completion("test prompt")
    
    assert result == "LLM says hello"
    agent_service.groq_client.chat.completions.create.assert_called_once()
