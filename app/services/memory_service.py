"""
Project memory service for storing and retrieving context
"""
from typing import List, Dict, Any, Optional
from app.database import get_supabase
import uuid


class MemoryService:
    """Service for managing project memory and context"""
    
    def __init__(self):
        self.supabase = get_supabase()
    
    async def store_conversation(self, project_id: str, role: str, content: str, metadata: Dict = None):
        """Store a conversation message"""
        memory_id = str(uuid.uuid4())
        
        memory_data = {
            "id": memory_id,
            "project_id": project_id,
            "item_type": "conversation",
            "content": content,
            "metadata": {
                "role": role,
                "timestamp": "now()",
                **(metadata or {})
            }
        }
        
        self.supabase.table("memory_items").insert(memory_data).execute()
    
    async def store_decision(self, project_id: str, decision: str, rationale: str, components: List[str]):
        """Store a coding decision"""
        memory_id = str(uuid.uuid4())
        
        memory_data = {
            "id": memory_id,
            "project_id": project_id,
            "item_type": "decision",
            "content": f"Decision: {decision}\nRationale: {rationale}",
            "metadata": {
                "decision": decision,
                "rationale": rationale,
                "affected_components": components,
                "timestamp": "now()"
            }
        }
        
        self.supabase.table("memory_items").insert(memory_data).execute()
    
    async def store_pattern(self, project_id: str, pattern_name: str, pattern_code: str, usage_context: str):
        """Store a code pattern"""
        memory_id = str(uuid.uuid4())
        
        memory_data = {
            "id": memory_id,
            "project_id": project_id,
            "item_type": "pattern",
            "content": f"Pattern: {pattern_name}\nCode: {pattern_code}\nContext: {usage_context}",
            "metadata": {
                "pattern_name": pattern_name,
                "usage_context": usage_context,
                "timestamp": "now()"
            }
        }
        
        self.supabase.table("memory_items").insert(memory_data).execute()
    
    async def store_preference(self, project_id: str, key: str, value: str):
        """Store a user preference"""
        memory_id = str(uuid.uuid4())
        
        memory_data = {
            "id": memory_id,
            "project_id": project_id,
            "item_type": "preference",
            "content": f"{key}: {value}",
            "metadata": {
                "key": key,
                "value": value,
                "timestamp": "now()"
            }
        }
        
        self.supabase.table("memory_items").insert(memory_data).execute()
    
    async def get_project_memory(self, project_id: str, item_type: Optional[str] = None) -> List[Dict]:
        """Get all memory items for a project"""
        query = self.supabase.table("memory_items")\
            .select("*")\
            .eq("project_id", project_id)\
            .order("created_at", desc=True)
        
        if item_type:
            query = query.eq("item_type", item_type)
        
        response = query.execute()
        return response.data
    
    async def search_memory(self, project_id: str, query: str, limit: int = 10) -> List[Dict]:
        """Search memory items by content (simple text search for now)"""
        response = self.supabase.table("memory_items")\
            .select("*")\
            .eq("project_id", project_id)\
            .ilike("content", f"%{query}%")\
            .order("created_at", desc=True)\
            .limit(limit)\
            .execute()
        
        return response.data


# Singleton instance
memory_service = MemoryService()