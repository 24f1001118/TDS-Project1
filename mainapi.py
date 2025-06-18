from fastapi import FastAPI, Request
from pydantic import BaseModel
from qa_engine import get_best_answer
import base64
import os

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QARequest(BaseModel):
    question: str
    image: str | None = None  # base64 image is optional

@app.post("/api/")
async def answer_question(data: QARequest):
    answer = get_best_answer(data.question, data.image)
    return {"answer": answer["answer"], "links": answer["links"]}
