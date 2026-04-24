from pydantic import BaseModel, Field


class TickerResult(BaseModel):
    ticker: str = Field(
        ...,
        description="Stock Ticker symbol (1-5 uppercase letters)",
        pattern="^[A-Z]{1,5}$",
    )
