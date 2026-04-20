from groq import Groq
from api.config.settings import settings
from api.models.rag import RAGResponse
from api.services.search import SearchService


class RAGService:
    def __init__(self, search_service: SearchService):
        self.client = Groq(api_key=settings.groq_api_key)
        self.search_service = search_service

    def generate_answer(self, query: str, limit: int = 3) -> RAGResponse:
        search_response = self.search_service.search(query, limit)
        context = "\n\n".join(result.text for result in search_response.results)
        prompt = f"""Based on the context provided, answer the following question.
        
        Context:
        {context}
        
        Question: {query}
        Answer:
        """

        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=settings.groq_model,
            temperature=0,
        )

        metadata = [
            {
                **result.metadata,
                "score": result.score,
            }
            for result in search_response.results
        ]
        return RAGResponse(
            query=query,
            answer=response.choices[0].message.content,
            metadata=metadata,
        )
