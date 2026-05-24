"""FastAPI 客户支持后端接口"""

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from langgraph_customer_support.graph import graph

app = FastAPI(title="Customer Support API")


class ChatRequest(BaseModel):
    """用户查询请求体"""

    query: str


class ChatResponse(BaseModel):
    """工作流返回结果"""

    query: str
    category: str
    sentiment: str
    response: str


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """接收用户问题，执行 LangGraph 工作流并返回结果"""
    result = graph.invoke({"query": req.query})
    return ChatResponse(**result)


@app.get("/")
async def index():
    """返回聊天页面"""
    return FileResponse("src/static/index.html")


app.mount("/static", StaticFiles(directory="src/static"), name="static")
