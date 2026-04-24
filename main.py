from fastapi import FastAPI
from api.routers import search, rag, health, ingest, agent

app = FastAPI(title="Financial Search API")

app.include_router(health.router)
app.include_router(search.router)
app.include_router(rag.router)
app.include_router(ingest.router)
app.include_router(agent.router)

