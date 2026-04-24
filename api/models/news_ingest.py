from pydantic import BaseModel, Field
from typing import Optional


class NewsIngestRequest(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol")
    max_stories: Optional[int] = Field(
        10, description="Maximum number of news stories to fetch"
    )

    model_config = {
        "json_schema_extra": {"examples": [{"ticker": "AAPL", "max_stories": 10}]}
    }
