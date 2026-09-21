from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from services.snaptrade_service import snaptrade_service

router = APIRouter(prefix="/api/auth", tags=["auth"])

class UserRegisterRequest(BaseModel):
    user_id: str

class LoginUrlRequest(BaseModel):
    user_id: str
    user_secret: str

@router.post("/register")
async def register_user(req: UserRegisterRequest):
    """Register user with SnapTrade or return demo session."""
    try:
        res = await snaptrade_service.register_user(req.user_id)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login-url")
async def get_login_url(req: LoginUrlRequest):
    """Obtain SnapTrade Connection Portal URL."""
    try:
        res = await snaptrade_service.get_connection_portal_url(req.user_id, req.user_secret)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
