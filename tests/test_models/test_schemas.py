import pytest
from pydantic import ValidationError
from api.models.agent import AgentRequest, AgentResponse
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
    res = AgentResponse(
        ticker="AAPL",
        final_recommendation="Hold",
        fundamental_analysis="...",
        momentum_analysis="...",
        sentiment_analysis="..."
    )
    data = res.model_dump()
    assert data["ticker"] == "AAPL"
    assert "final_recommendation" in data
