import instructor
from groq import Groq
from api.config.settings import settings
from api.models.ticker_result import TickerResult
from api.config.prompts.company_mappings import (
    TICKER_EXTRACTION_PROMPT,
    COMPANY_TICKER_MAPPINGS,
)


class TickerExtractionService:
    def __init__(self):
        self.groq_client = Groq(api_key=settings.groq_api_key)
        self.client = instructor.from_groq(self.groq_client, mode=instructor.Mode.JSON)
        self.company_ticker_mappings = COMPANY_TICKER_MAPPINGS

    def extract_ticker(self, query: str) -> str | None:
        query_lower = query.lower()

        for company, ticker in self.company_ticker_mappings.items():
            if company in query_lower or ticker.lower() in query_lower:
                return ticker

        return self._extract_with_llm(query)

    def _extract_with_llm(self, query: str) -> str | None:
        try:
            response = self.client.chat.completions.create(
                model=settings.groq_model,
                messages=[
                    {"role": "system", "content": TICKER_EXTRACTION_PROMPT},
                    {"role": "user", "content": query},
                ],
                temperature=0,
                response_model=TickerResult,
            )
            return response.ticker if response.ticker != "NONE" else None
        except Exception as e:
            print(f"Ticker extraction failed: {e}")
            return None
