from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag import answer

app = FastAPI(title="RAG 知识库问答接口")

class AskRequest(BaseModel):
    """请求体：只接收一个question字段"""
    question: str
    top_k: int=3

class AskResponse(BaseModel):
    """响应体：答案+来源"""
    answer: str
    sources: list[str]

@app.post("/ask")
def ask(req: AskRequest):
    try:
        text,hits = answer(req.question)
        return AskResponse(
            answer=text,
            sources=[h["source"] for h in hits]
        )
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"处理失败:{e}")

@app.get("/health")
def health():
    return {"status":"ok"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)