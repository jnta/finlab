from typing import Optional, Dict, Any
from typing import List
from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(..., description="The search query")
    limit: int = Field(3, description="Maximum number of results to return")
    filters: Optional[Dict[str, Any]] = Field(
        None, description="Filters to apply to the search"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "query": "What are Apple's main risks?",
                    "limit": 5,
                    "filters": {
                        "ticker": "AAPL",
                        "form_type": "10-K",
                        "source": "yahoo_finance",
                    },
                }
            ]
        }
    }


class SearchResult(BaseModel):
    score: float = Field(..., description="Search relevance score")
    text: str = Field(..., description="The content snippet")
    metadata: dict = Field(..., description="Additional metadata")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "score": 0.89,
                    "text": "Apple faces supply chain challenges in Asia...",
                    "metadata": {"ticker": "AAPL", "source": "news"},
                }
            ]
        }
    }


class SearchResponse(BaseModel):
    results: List[SearchResult] = Field(..., description="List of search results")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "results": [
                        {
                            "score": 0.89,
                            "text": "Apple faces supply chain challenges in Asia...",
                            "metadata": {"ticker": "AAPL", "source": "news"},
                        }
                    ]
                }
            ]
        }
    }
