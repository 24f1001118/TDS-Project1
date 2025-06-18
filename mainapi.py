from fastapi import FastAPI, Request
from pydantic import BaseModel
from qa_engine import get_best_answer
import base64
import os

app = FastAPI()

class QARequest(BaseModel):
    question: str
    image: str | None = None  # base64 image is optional

@app.post("/api/")
async def answer_question(data: QARequest):
    answer = get_best_answer(data.question, data.image)
    return {"answer": answer}
