from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models import ChatMessage, ChatMessageResponse, User
from app.auth import get_current_user

router = APIRouter()


@router.post("", response_model=ChatMessageResponse)
async def send_message(
    project_id: str,
    message: ChatMessage,
    current_user: User = Depends(get_current_user)
):
    """Send a message to the AI assistant"""
    # TODO: Implement AI chat functionality
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/history", response_model=List[ChatMessageResponse])
async def get_chat_history(
    project_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get chat history for a project"""
    # TODO: Implement chat history retrieval
    return []
