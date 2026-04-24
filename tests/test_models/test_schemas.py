import pytest
from pydantic import ValidationError
from api.models.agent import (
    AgentRequest,
    AgentResponse,
    FundamentalAnalysis,
    MomentumAnalysis,
    SentimentAnalysis,
    FinalRecommendation,
)
from api.models.search import SearchRequest


def test_agent_request_validation():
    # Valid
    req = AgentRequest(ticker="MSFT", limit=10)
    assert req.ticker == "MSFT"
    assert req.limit == 10

    # Default limit
    req = AgentRequest(ticker="TSLA")
    assert req.limit == 3

    # Invalid: missing ticker
    with pytest.raises(ValidationError):
        AgentRequest()


def test_search_request_validation():
    # Valid
    req = SearchRequest(query="test", limit=5, filters={"key": "val"})
    assert req.query == "test"

    # Invalid: missing query
    with pytest.raises(ValidationError):
        SearchRequest(limit=5)


def test_agent_response_serialization():
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

    res = AgentResponse(
        ticker="AAPL",
        final_recommendation=final,
        fundamental_analysis=fundamental,
        momentum_analysis=momentum,
        sentiment_analysis=sentiment,
    )
    data = res.model_dump()
    assert data["ticker"] == "AAPL"
    assert data["final_recommendation"]["action"] == "BUY"
