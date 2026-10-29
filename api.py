"""FastAPI service for the mortgage assistant."""
from fastapi import FastAPI
from pydantic import BaseModel
from assistant.bot import ask

app = FastAPI(title="Northfield Harbour Mortgage Assistant")


class AskRequest(BaseModel):
    question: str


class ChunkSummary(BaseModel):
    source: str
    text: str


class AskResponse(BaseModel):
    answer: str
    citations: list[str]
    retrieved_chunks: list[ChunkSummary]


@app.post("/ask", response_model=AskResponse)
def ask_endpoint(req: AskRequest) -> AskResponse:
    result = ask(req.question)
    return AskResponse(
        answer=result["answer"],
        citations=result["citations"],
        retrieved_chunks=[ChunkSummary(**c) for c in result["retrieved_chunks"]],
    )
