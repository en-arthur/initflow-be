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
    from app.services.memory_service import memory_service
    
    user_message_id = str(uuid.uuid4())
    user_message_data = {
        "id": user_message_id,
        "project_id": project_id,
        "role": "user",
        "content": message.message,
        "attachments": None,
    }
    
    supabase.table("chat_messages").insert(user_message_data).execute()
    
    # Store in memory
    await memory_service.store_conversation(project_id, "user", message.message)
    
    # Generate AI response with context using tier-based models
    from app.services.ai_service import ai_service
    
    # Get project context for AI
    project_context = {
        "project_info": project_info,
        "recent_memory": recent_memory[:5],  # Last 5 memory items
        "spec_context": spec_context
    }
    
    ai_response = await ai_service.generate_response(
        current_user, 
        message.message, 
        context=project_context,
        system_prompt="You are an expert mobile app development assistant specializing in React Native and Expo."
    )
    
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
    
    # Store AI response in memory
    await memory_service.store_conversation(project_id, "assistant", ai_response)
    
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
    """Generate AI response with project context"""
    from app.services.memory_service import memory_service
    
    # Get project context
    supabase = get_supabase()
    
    # Get project info
    project = supabase.table("projects").select("name, description").eq("id", project_id).execute()
    project_info = project.data[0] if project.data else {}
    
    # Get recent memory for context
    recent_memory = await memory_service.get_project_memory(project_id)
    
    # Get spec files for context
    specs = supabase.table("spec_files").select("file_type, content").eq("project_id", project_id).execute()
    spec_context = {spec["file_type"]: spec["content"][:500] + "..." for spec in specs.data}
    
    message_lower = user_message.lower()
    
    # Context-aware responses
    if any(word in message_lower for word in ["hello", "hi", "hey"]):
        project_name = project_info.get("name", "your project")
        return f"Hello! I'm your AI assistant for {project_name}. I can see you're working on a mobile app project. I can help you add features, fix bugs, refactor code, explain architecture, or generate new components. What would you like to work on?"
    
    elif "add feature" in message_lower or "new feature" in message_lower:
        return f"I'd be happy to help you add a new feature to your app! Based on your project specs, I can generate the necessary code and update your specifications. What specific feature would you like to add? For example:\n\n• User authentication\n• Data storage\n• API integration\n• UI components\n• Navigation screens"
    
    elif "fix bug" in message_lower or "error" in message_lower or "issue" in message_lower:
        return "I can help you debug and fix issues in your code. Could you describe:\n\n• What error are you seeing?\n• Which part of the app is affected?\n• What were you trying to do when it happened?\n\nI'll analyze your code and suggest a fix!"
    
    elif "refactor" in message_lower or "improve" in message_lower:
        return "I can help refactor your code to make it cleaner and more maintainable. Which area would you like to improve?\n\n• Component structure\n• State management\n• Performance optimization\n• Code organization\n• Best practices implementation"
    
    elif "explain" in message_lower or "how does" in message_lower or "what is" in message_lower:
        return "I can explain any part of your app's architecture or code. What would you like me to explain?\n\n• Overall app structure\n• Specific components\n• Data flow\n• Navigation setup\n• API integration\n• State management"
    
    elif "specs" in message_lower or "specification" in message_lower:
        return f"I can see your project has specification files. Here's what I found:\n\n• Design specs: {'✓' if 'design' in spec_context else '✗'}\n• Requirements: {'✓' if 'requirements' in spec_context else '✗'}\n• Tasks: {'✓' if 'tasks' in spec_context else '✗'}\n\nWould you like me to update any of these specs or generate code based on them?"
    
    elif "deploy" in message_lower or "publish" in message_lower:
        return "I can help you prepare your app for deployment! Here's what we need to do:\n\n• Build the app for production\n• Generate app store assets\n• Configure app signing\n• Create store listings\n• Submit to App Store/Google Play\n\nWhich step would you like to start with?"
    
    else:
        # Try to be helpful with context
        context_hint = ""
        if project_info.get("description"):
            context_hint = f" I can see you're building {project_info['description']}."
        
        return f"I understand you're asking about: '{user_message}'.{context_hint} I can help you with:\n\n• Adding new features\n• Fixing bugs and issues\n• Refactoring code\n• Explaining architecture\n• Updating specifications\n• Preparing for deployment\n\nCould you be more specific about what you'd like to do?"
