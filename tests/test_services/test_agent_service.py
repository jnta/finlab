import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from api.services.agent import AgentService
from api.models.agent import (
    AgentResponse,
    FundamentalAnalysis,
    MomentumAnalysis,
    SentimentAnalysis,
    FinalRecommendation,
)
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
    # Mock return values for different analyses
    fundamental = FundamentalAnalysis(
        overall_investment_thesis="Good",
        investment_grade="A",
        confidence_score=0.9,
        key_strengths=["S1", "S2", "S3"],
        key_concerns=["C1", "C2", "C3"],
        recommendation="buy",
    )
    momentum = MomentumAnalysis(
        overall_momentum="positive",
        momentum_strength="strong",
        key_momentum_drivers=["D1", "D2"],
        momentum_risks=["R1", "R2"],
        short_term_outlook="bullish",
        momentum_score=8.5,
    )
    sentiment = SentimentAnalysis(
        sentiment_score=8.0,
        sentiment_direction="Positive",
        key_news_themes=["T1"],
        recent_catalysts=["Cat1"],
        market_outlook="Bullish",
    )
    final = FinalRecommendation(
        action="BUY",
        confidence=0.9,
        rationale="Strong indicators",
        key_risks=["R1"],
        key_opportunities=["O1"],
        time_horizon="Medium-term",
    )

    # Mock _generate_completion to return these models in order
    agent_service._generate_completion = AsyncMock(side_effect=[
        fundamental, momentum, sentiment, final
    ])

    response = await agent_service.analyze(ticker="AAPL", limit=1)

    assert isinstance(response, AgentResponse)
    assert response.ticker == "AAPL"
    assert response.fundamental_analysis.investment_grade == "A"
    
    # Verify search service was called
    assert agent_service.search_service.search.called

    # Verify _generate_completion was called 4 times
    assert agent_service._generate_completion.call_count == 4

@pytest.mark.asyncio
async def test_generate_completion(agent_service):
    agent_service.groq_client = AsyncMock()
    # When instructor is used, it returns the model instance directly
    mock_model = MagicMock(spec=FundamentalAnalysis)
    agent_service.groq_client.chat.completions.create.return_value = mock_model

    result = await agent_service._generate_completion("test prompt", FundamentalAnalysis)
    
    assert result == mock_model
    agent_service.groq_client.chat.completions.create.assert_called_once()
