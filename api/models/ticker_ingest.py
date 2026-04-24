from pydantic import BaseModel, Field

class TickerIngestRequest(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ticker": "AAPL"
                }
            ]
        }
    }

class IngestResponse(BaseModel):
    message: str = Field(..., description="Status message")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "Successfully ingested data for AAPL"
                }
            ]
        }
    }
