from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.models import ChatMessage, ChatMessageResponse, User
from app.auth import get_current_user
from app.database import get_supabase
import uuid

router = APIRouter()


@router.post("", response_model=ChatMessageResponse)
async def send_message(
    project_id: str,
    message: ChatMessage,
    current_user: User = Depends(get_current_user)
):
    """Send a message to the AI assistant"""
    supabase = get_supabase()
    
    # Verify project access
    project_response = supabase.table("projects")\
        .select("user_id")\
        .eq("id", project_id)\
        .execute()
    
    if not project_response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    if project_response.data[0]["user_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Store user message
    import uuid
    from datetime import datetime
    
    user_message_id = str(uuid.uuid4())
    user_message_data = {
        "id": user_message_id,
        "project_id": project_id,
        "role": "user",
        "content": message.message,
        "attachments": None,
    }
    
    supabase.table("chat_messages").insert(user_message_data).execute()
    
    # Generate AI response (simplified for now)
    ai_response = await generate_ai_response(message.message, project_id)
    
    # Store AI message
    ai_message_id = str(uuid.uuid4())
    ai_message_data = {
        "id": ai_message_id,
        "project_id": project_id,
        "role": "assistant",
        "content": ai_response,
        "attachments": None,
    }
    
    ai_message_response = supabase.table("chat_messages").insert(ai_message_data).execute()
    
    return ChatMessageResponse(**ai_message_response.data[0])


@router.get("/history", response_model=List[ChatMessageResponse])
async def get_chat_history(
    project_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get chat history for a project"""
    supabase = get_supabase()
    
    # Verify project access
    project_response = supabase.table("projects")\
        .select("user_id")\
        .eq("id", project_id)\
        .execute()
    
    if not project_response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    if project_response.data[0]["user_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Get chat messages
    messages_response = supabase.table("chat_messages")\
        .select("*")\
        .eq("project_id", project_id)\
        .order("created_at", desc=False)\
        .execute()
    
    return [ChatMessageResponse(**msg) for msg in messages_response.data]


async def generate_ai_response(user_message: str, project_id: str) -> str:
    """Generate AI response (simplified implementation)"""
    # This is a placeholder implementation
    # In the full version, this would integrate with OpenAI/Anthropic
    # and use project context, specs, and memory
    
    responses = {
        "hello": "Hello! I'm your AI assistant. I can help you build your mobile app by adding features, fixing bugs, refactoring code, and explaining how things work. What would you like to do?",
        "add feature": "I'd be happy to help you add a new feature! Could you describe what feature you'd like to add to your app?",
        "fix bug": "I can help you fix bugs in your code. Could you describe the issue you're experiencing?",
        "refactor": "I can help refactor your code to make it cleaner and more maintainable. Which part of the code would you like me to refactor?",
        "explain": "I can explain any part of your code or app architecture. What would you like me to explain?",
    }
    
    message_lower = user_message.lower()
    
    for key, response in responses.items():
        if key in message_lower:
            return response
    
    return f"I understand you said: '{user_message}'. I'm still learning how to help with this specific request. In the full version, I'll be able to analyze your project specs, generate code, and provide detailed assistance. For now, try asking me to 'add feature', 'fix bug', 'refactor', or 'explain' something!"
