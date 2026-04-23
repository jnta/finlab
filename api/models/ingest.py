from pydantic import BaseModel

class IngestRequest(BaseModel):
    ticker: str

class IngestResponse(BaseModel):
    message: str
