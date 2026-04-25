import pytest
from unittest.mock import MagicMock, patch
from api.services.search import SearchService
from api.models.search import SearchResponse

@pytest.fixture
def search_service():
    with patch("api.services.search.QdrantClient"), \
         patch("api.services.search.EmbeddingsService") as mock_embeddings:
        # Mock embedding return values
        mock_embeddings.return_value.embed_query.return_value = ([0.1]*384, [0.2]*384, [0.3]*384)
        service = SearchService(qdrant_url="http://fake", qdrant_api_key="fake", collection_name="test")
        return service

def test_build_filter_clauses(search_service):
    filters = {"ticker": "AAPL", "form_type": "10-K"}
    expected = {
        "must": [
            {"key": "metadata.ticker", "match": {"value": "AAPL"}},
            {"key": "metadata.form_type", "match": {"value": "10-K"}}
        ]
    }
    result = search_service._build_filter_clauses(filters)
    assert result == expected

def test_build_filter_clauses_empty(search_service):
    assert search_service._build_filter_clauses(None) is None
    assert search_service._build_filter_clauses({}) is None

def test_search_mapping(search_service):
    # Mock Qdrant results
    mock_point = MagicMock()
    mock_point.score = 0.8
    mock_point.payload = {"text": "test content", "metadata": {"source": "test"}}
    
    search_service.qdrant.query_points.return_value = MagicMock(points=[mock_point])
    
    response = search_service.search("test query", limit=1)
    
    assert isinstance(response, SearchResponse)
    assert len(response.results) == 1
    assert response.results[0].text == "test content"
    assert response.results[0].score == 1.0  # Normalized (0.8 / 0.8)

def test_search_empty_results(search_service):
    search_service.qdrant.query_points.return_value = MagicMock(points=[])
    
    response = search_service.search("test query")
    
    assert isinstance(response, SearchResponse)
    assert len(response.results) == 0
