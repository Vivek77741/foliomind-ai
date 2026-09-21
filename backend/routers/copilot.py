from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
from services.ai_agent import ai_agent

router = APIRouter(prefix="/api/copilot", tags=["copilot"])

class ChatRequest(BaseModel):
    query: str
    user_id: str = "demo_user"
    user_secret: str = "mock_secret_demo_user"
    chat_history: Optional[List[Dict[str, str]]] = None

@router.post("/chat")
async def chat_copilot(req: ChatRequest):
    """Process natural language queries via grounded AI agent."""
    try:
        res = await ai_agent.process_user_query(
            query=req.query,
            user_id=req.user_id,
            user_secret=req.user_secret,
            chat_history=req.chat_history
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
