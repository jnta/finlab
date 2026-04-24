from typing import List, Literal

from pydantic import BaseModel, Field


class FundamentalAnalysis(BaseModel):
    overall_investment_thesis: str = Field(..., description="Overall investment thesis")
    investment_grade: Literal["A", "B", "C", "D"] = Field(
        ..., description="Investment grade"
    )
    confidence_score: float = Field(
        ..., ge=0.0, le=1.0, description="Confidence score between 0 and 1"
    )
    key_strengths: List[str] = Field(
        min_len=3, max_len=3, description="Key strengths of the investment"
    )
    key_concerns: List[str] = Field(
        min_len=3, max_len=3, description="Key concerns of the investment"
    )
    recommendation: Literal["buy", "hold", "sell", "avoid"]


class MomentumAnalysis(BaseModel):
    overall_momentum: Literal["positive", "neutral", "negative"] = Field(
        ..., description="Overall momentum"
    )
    momentum_strength: Literal["strong", "moderate", "weak"] = Field(
        ..., description="Momentum strength"
    )
    key_momentum_drivers: List[str] = Field(
        min_length=2, max_length=3, description="Key momentum drivers"
    )
    momentum_risks: List[str] = Field(
        min_length=2, max_length=3, description="Momentum risks"
    )
    short_term_outlook: Literal["bullish", "neutral", "bearish"] = Field(
        ..., description="Short term outlook"
    )
    momentum_score: float = Field(
        ..., ge=0, le=10, description="Momentum score between 0 and 10"
    )


class SentimentAnalysis(BaseModel):
    sentiment_score: float = Field(
        ..., ge=1, le=10, description="Sentiment score between 1 and 10"
    )
    sentiment_direction: Literal["Positive", "Neutral", "Negative"] = Field(
        ..., description="Sentiment direction"
    )
    key_news_themes: List[str] = Field(
        ..., min_length=1, max_length=5, description="Key news themes"
    )
    recent_catalysts: List[str] = Field(
        ..., min_length=1, max_length=5, description="Recent catalysts"
    )
    market_outlook: str = Field(..., description="Market outlook")


class FinalRecommendation(BaseModel):
    action: Literal["BUY", "HOLD", "SELL"] = Field(
        ..., description="Recommended action"
    )
    confidence: float = Field(
        ge=0, le=1, description="Confidence score between 0 and 1"
    )
    rationale: str = Field(..., description="Rationale for recommendation")
    key_risks: List[str] = Field(
        ..., description="Key risks associated with the recommendation"
    )
    key_opportunities: List[str] = Field(
        ..., description="Key opportunities associated with the recommendation"
    )
    time_horizon: Literal["Short-term", "Medium-term", "Long-term"] = Field(
        ..., description="Time horizon for the recommendation"
    )


class AgentRequest(BaseModel):
    ticker: str = Field(
        ...,
        description="Stock ticker symbol (e.g., AAPL, TSLA)",
        min_length=1,
        max_length=10,
    )
    limit: int = Field(
        3,
        description="Number of context chunks to retrieve for each analysis type",
        ge=1,
        le=10,
    )

    model_config = {"json_schema_extra": {"examples": [{"ticker": "AAPL", "limit": 3}]}}


class AgentResponse(BaseModel):
    ticker: str = Field(..., description="The ticker symbol analyzed")
    fundamental_analysis: FundamentalAnalysis = Field(
        ..., description="LLM-generated fundamental analysis"
    )
    momentum_analysis: MomentumAnalysis = Field(
        ..., description="LLM-generated momentum and technical analysis"
    )
    sentiment_analysis: SentimentAnalysis = Field(
        ..., description="LLM-generated sentiment analysis from recent news"
    )
    final_recommendation: FinalRecommendation = Field(
        ..., description="The synthesized investment recommendation"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ticker": "AAPL",
                    "fundamental_analysis": {
                        "overall_investment_thesis": "Apple displays robust revenue growth driven by services and iPhone 15 demand...",
                        "investment_grade": "A",
                        "confidence_score": 0.95,
                        "key_strengths": [
                            "Strong brand loyalty",
                            "Ecosystem lock-in",
                            "Consistent revenue growth",
                        ],
                        "key_concerns": [
                            "Supply chain risks",
                            "Regulatory scrutiny",
                            "Over-reliance on iPhone sales",
                        ],
                        "recommendation": "BUY",
                    },
                    "momentum_analysis": {
                        "overall_momentum": "positive",
                        "momentum_strength": "strong",
                        "key_momentum_drivers": [
                            "Strong earnings growth",
                            "Positive analyst revisions",
                        ],
                        "momentum_risks": [
                            "Supply chain constraints",
                            "Geopolitical tensions",
                        ],
                        "short_term_outlook": "bullish",
                        "momentum_score": 9.5,
                    },
                    "sentiment_analysis": {
                        "sentiment_score": 9.0,
                        "sentiment_direction": "Positive",
                        "key_news_themes": [
                            "Strong earnings",
                            "New product launches",
                            "Positive analyst ratings",
                        ],
                        "recent_catalysts": ["Strong iPhone sales", "Services growth"],
                        "market_outlook": "Positive",
                    },
                    "final_recommendation": {
                        "action": "BUY",
                        "confidence": 0.95,
                        "rationale": "Strong Buy based on convergent fundamental and technical indicators.",
                        "key_risks": [
                            "Supply chain risks",
                            "Regulatory scrutiny",
                            "Over-reliance on iPhone sales",
                        ],
                        "key_opportunities": [
                            "Strong brand loyalty",
                            "Ecosystem lock-in",
                            "Consistent revenue growth",
                        ],
                        "time_horizon": "Short-term",
                    },
                }
            ]
        }
    }
