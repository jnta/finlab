from pydantic import BaseModel, Field


class RAGRequest(BaseModel):
    query: str = Field(..., description="The user query to answer")
    limit: int = Field(3, description="Number of context chunks to retrieve")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "query": "Is Tesla's growth sustainable?",
                    "limit": 3
                }
            ]
        }
    }


class RAGResponse(BaseModel):
    query: str = Field(..., description="The original query")
    answer: str = Field(..., description="The AI generated answer")
    metadata: list[dict] = Field(..., description="Metadata from retrieved chunks")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "query": "Is Tesla's growth sustainable?",
                    "answer": "Based on recent earnings, Tesla's growth is driven by expanding production capacity...",
                    "metadata": [{"ticker": "TSLA", "source": "Q3 Report"}]
                }
            ]
        }
    }
