import pytest
from unittest.mock import AsyncMock, patch
from api.models.agent import AgentResponse

@pytest.mark.asyncio
async def test_analyze_endpoint(client):
    mock_response = AgentResponse(
        ticker="AAPL",
        final_recommendation="Buy",
        fundamental_analysis="Good",
        momentum_analysis="Strong",
        sentiment_analysis="Positive"
    )
    
    with patch("api.routers.agent.agent_service.analyze", new_callable=AsyncMock) as mock_analyze:
        mock_analyze.return_value = mock_response
        
        response = client.post("/agent/analyze", json={"ticker": "AAPL", "limit": 3})
        
        assert response.status_code == 200
        data = response.json()
        assert data["ticker"] == "AAPL"
        assert data["final_recommendation"] == "Buy"
        mock_analyze.assert_called_once_with(ticker="AAPL", limit=3)

def test_analyze_validation_error(client):
    # Missing ticker
    response = client.post("/agent/analyze", json={"limit": 3})
    assert response.status_code == 422
