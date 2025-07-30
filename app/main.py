from app.query import answer_with_context
from app.rephrase_agent import rephrase_user_query
from app.api import openrouter_api, QDRANT_API_KEY, QDRANT_URL, COLLECTION_NAME
from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"message": "App is running"}

@app.post("/ask")
def proceed_user_query(request: QueryRequest):
    limit = 7
    user_query = request.question
    rephrased_query = rephrase_user_query(user_query)
    try:
        ans = answer_with_context(rephrased_query, COLLECTION_NAME, limit)
        return {"question": user_query, "answer": ans}
    except Exception as e:
        print(f"Ошибка: {e}")
    



