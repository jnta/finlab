from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol (e.g., AAPL, TSLA)", min_length=1, max_length=10)
    limit: int = Field(3, description="Number of context chunks to retrieve for each analysis type", ge=1, le=10)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ticker": "AAPL",
                    "limit": 3
                }
            ]
        }
    }


class AgentResponse(BaseModel):
    ticker: str = Field(..., description="The ticker symbol analyzed")
    fundamental_analysis: str = Field(..., description="LLM-generated fundamental analysis")
    momentum_analysis: str = Field(..., description="LLM-generated momentum and technical analysis")
    sentiment_analysis: str = Field(..., description="LLM-generated sentiment analysis from recent news")
    final_recommendation: str = Field(..., description="The synthesized investment recommendation")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ticker": "AAPL",
                    "fundamental_analysis": "Apple displays robust revenue growth driven by services and iPhone 15 demand...",
                    "momentum_analysis": "The stock shows strong bullish momentum with support at $180...",
                    "sentiment_analysis": "Overall market sentiment is high following positive analyst reports...",
                    "final_recommendation": "Strong Buy based on convergent fundamental and technical indicators."
                }
            ]
        }
    }
