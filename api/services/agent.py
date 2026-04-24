from api.models.agent import FinalRecommendation
import asyncio
from typing import Any, Dict, List

import instructor
from groq import AsyncGroq

from api.config.prompts.aggregation import AGGREGATION_PROMPT
from api.config.prompts.fundamental import FUNDAMENTAL_PROMPT
from api.config.prompts.momentum import MOMENTUM_PROMPT
from api.config.prompts.sentiment import SENTIMENT_PROMPT
from api.config.queries.fundamental import FUNDAMENTAL_QUERIES
from api.config.queries.momentum import MOMENTUM_QUERIES
from api.config.queries.sentiment import SENTIMENT_QUERY_TEMPLATE
from api.config.settings import settings
from api.models.agent import (
    AgentResponse,
    FundamentalAnalysis,
    MomentumAnalysis,
    SentimentAnalysis,
)
from api.services.search import SearchService


class AgentService:
    def __init__(self, search_service: SearchService):
        self.search_service = search_service
        self.groq_client = AsyncGroq(api_key=settings.groq_api_key)
        self.client = instructor.from_groq(self.groq_client, mode=instructor.Mode.JSON)

    def _run_queries(self, queries: list[str], limit: int, filter: Dict[str, Any]):
        all_results = []
        for query in queries:
            search_results = self.search_service.search(query, limit, filter)
            all_results.extend([result.text for result in search_results.results])
        return "\n\n".join(all_results)

    async def _generate_completion(self, prompt: str, response_model=None):
        return await self.groq_client.chat.completions.create(
            model=settings.groq_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            response_model=response_model,
        )

    async def _analyze_fundamental(self, ticker: str, limit: int):
        filter = {"ticker": ticker, "form_type": "10-K"}
        context = self._run_queries(FUNDAMENTAL_QUERIES, limit, filter)
        prompt = FUNDAMENTAL_PROMPT.format(context=context)
        return await self._generate_completion(prompt, FundamentalAnalysis)

    async def _analyze_momentum(self, ticker: str, limit: int):
        filter = {"ticker": ticker, "form_type": "10-Q"}
        context = self._run_queries(MOMENTUM_QUERIES, limit, filter)
        prompt = MOMENTUM_PROMPT.format(context=context)
        return await self._generate_completion(prompt, MomentumAnalysis)

    async def _analyze_sentiment(self, ticker: str, limit: int):
        query = SENTIMENT_QUERY_TEMPLATE.format(ticker=ticker)
        filter = {"ticker": ticker, "source": "yahoo_finance"}
        context = self._run_queries([query], limit, filter)
        prompt = SENTIMENT_PROMPT.format(context=context, ticker=ticker)
        return await self._generate_completion(prompt, SentimentAnalysis)

    async def analyze(self, ticker: str, limit: int = 3):
        (
            fundamental_analysis,
            momentum_analysis,
            sentiment_analysis,
        ) = await asyncio.gather(
            self._analyze_fundamental(ticker, limit),
            self._analyze_momentum(ticker, limit),
            self._analyze_sentiment(ticker, limit),
        )
        aggregation_prompt = AGGREGATION_PROMPT.format(
            fundamental=fundamental_analysis.model_dump_json(indent=2),
            momentum=momentum_analysis.model_dump_json(indent=2),
            sentiment=sentiment_analysis.model_dump_json(indent=2),
        )
        final_recommendation = await self._generate_completion(
            aggregation_prompt, FinalRecommendation
        )
        return AgentResponse(
            ticker=ticker,
            final_recommendation=final_recommendation,
            fundamental_analysis=fundamental_analysis,
            momentum_analysis=momentum_analysis,
            sentiment_analysis=sentiment_analysis,
        )
