from fastapi import FastAPI
from pydantic import BaseModel
from investigation_copilot import get_investigation_response

app = FastAPI(title="Investigation Copilot API")


class QueryRequest(BaseModel):
    text: str


@app.post("/investigate")
def investigate(request: QueryRequest):
    """
    Takes a user query about a suspicious message/call, runs it through the
    Scam Classifier + RAG retrieval + LLM pipeline, and returns a structured
    investigation report along with the numeric scam data.
    """
    result = get_investigation_response(request.text)
    return result