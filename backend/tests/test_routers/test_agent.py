import pytest
from unittest.mock import AsyncMock, patch
from api.models.agent import (
    AgentResponse,
    FundamentalAnalysis,
    MomentumAnalysis,
    SentimentAnalysis,
    FinalRecommendation,
)


@pytest.mark.asyncio
async def test_analyze_endpoint(client):
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
    mock_response = AgentResponse(
        query="tell me about apple",
        ticker="AAPL",
        final_recommendation=final,
        fundamental_analysis=fundamental,
        momentum_analysis=momentum,
        sentiment_analysis=sentiment,
    )
    
    with patch("api.routers.agent.agent_service.analyze", new_callable=AsyncMock) as mock_analyze:
        mock_analyze.return_value = mock_response
        
        response = client.post("/agent/analyze", json={"query": "tell me about apple", "limit": 3})
        
        assert response.status_code == 200
        data = response.json()
        assert data["ticker"] == "AAPL"
        assert data["query"] == "tell me about apple"
        assert data["final_recommendation"]["action"] == "BUY"
        mock_analyze.assert_called_once_with("tell me about apple", 3)

def test_analyze_validation_error(client):
    # Missing query
    response = client.post("/agent/analyze", json={"limit": 3})
    assert response.status_code == 422
