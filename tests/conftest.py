import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from main import app
from api.services.search import SearchService
from api.services.agent import AgentService

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_search_service():
    service = MagicMock(spec=SearchService)
    return service

@pytest.fixture
def mock_agent_service():
    service = MagicMock(spec=AgentService)
    return service
