import pytest
from unittest.mock import MagicMock, patch
from api.models.search import SearchResponse, SearchResult

def test_search_endpoint(client):
    mock_results = SearchResponse(results=[
        SearchResult(score=0.9, text="Matching result", metadata={"source": "test"})
    ])
    
    with patch("api.routers.search.search_service.search") as mock_search:
        mock_search.return_value = mock_results
        
        payload = {
            "query": "What is the revenue?",
            "limit": 5,
            "filters": {"ticker": "AAPL"}
        }
        
        response = client.post("/search", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) == 1
        assert data["results"][0]["text"] == "Matching result"
        mock_search.assert_called_once_with(
            query="What is the revenue?",
            limit=5,
            filters={"ticker": "AAPL"}
        )

def test_search_validation_error(client):
    # Missing query
    response = client.post("/search", json={"limit": 5})
    assert response.status_code == 422
