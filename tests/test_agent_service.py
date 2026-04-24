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
    # Mock settings before instantiating service to avoid loading .env
    with patch("api.services.agent.settings") as mock_settings:
        mock_settings.groq_api_key = "fake_key"
        mock_settings.groq_model = "fake_model"
        return AgentService(search_service=mock_search_service)

@pytest.mark.asyncio
async def test_analyze_formatting(agent_service):
    """Test that the analyze method doesn't raise KeyError during formatting."""
    
    # Mock groq client
    agent_service.groq_client = AsyncMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Mocked LLM Response"
    agent_service.groq_client.chat.completions.create.return_value = mock_response

    # This should not raise KeyError
    response = await agent_service.analyze(ticker="AAPL", limit=1)

    assert isinstance(response, AgentResponse)
    assert response.ticker == "AAPL"
    assert response.final_recommendation == "Mocked LLM Response"
    
    # Verify that the completions were called 4 times (3 analysis + 1 aggregation)
    assert agent_service.groq_client.chat.completions.create.call_count == 4

@pytest.mark.asyncio
async def test_individual_analyses(agent_service):
    """Test that individual analysis methods format their prompts correctly."""
    agent_service.groq_client = AsyncMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Analysis Result"
    agent_service.groq_client.chat.completions.create.return_value = mock_response

    # Test fundamental
    res = await agent_service._analyze_fundamental(limit=1)
    assert res == "Analysis Result"

    # Test momentum
    res = await agent_service._analyze_momentum(limit=1)
    assert res == "Analysis Result"

    # Test sentiment
    res = await agent_service._analyze_sentiment(ticker="TSLA", limit=1)
    assert res == "Analysis Result"

@pytest.mark.asyncio
async def test_generate_completion_typos(agent_service):
    """Verify that _generate_completion uses correct client and methods."""
    agent_service.groq_client = AsyncMock()
    await agent_service._generate_completion("test prompt")
    
    # Check if correct method was called
    agent_service.groq_client.chat.completions.create.assert_called_once()
