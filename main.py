from fastapi import FastAPI
from api.routers import search, rag, health, ingest, agent

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Financial Search API")

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(search.router)
app.include_router(rag.router)
app.include_router(ingest.router)
app.include_router(agent.router)

