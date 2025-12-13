"""
Project memory service using Agno framework's memory capabilities
"""
from typing import List, Dict, Any, Optional
from agno.memory import Memory, MemoryItem
from app.database import get_supabase
import uuid
import json


class MemoryService:
    """Service for managing project memory using Agno framework"""
    
    def __init__(self):
        self.supabase = get_supabase()
        # Initialize Agno memory instances per project
        self._project_memories = {}
    
    def _get_project_memory(self, project_id: str) -> Memory:
        """Get or create Agno Memory instance for a project"""
        if project_id not in self._project_memories:
            # Initialize Agno Memory with project-specific configuration
            self._project_memories[project_id] = Memory(
                memory_id=f"project_{project_id}",
                storage_backend="supabase",  # Use Supabase as storage backend
                embedding_model="text-embedding-ada-002",  # For semantic search
                max_memory_items=1000,  # Limit memory items per project
                similarity_threshold=0.7
            )
        return self._project_memories[project_id]
    
    async def store_conversation(self, project_id: str, role: str, content: str, metadata: Dict = None):
        """Store a conversation message using Agno Memory"""
        memory = self._get_project_memory(project_id)
        
        # Create memory item with Agno
        memory_item = MemoryItem(
            content=content,
            metadata={
                "type": "conversation",
                "role": role,
                "project_id": project_id,
                **(metadata or {})
            },
            importance_score=0.8 if role == "assistant" else 0.6  # AI responses are more important
        )
        
        # Store in Agno memory
        await memory.add(memory_item)
        
        # Also store in Supabase for persistence
        await self._store_in_supabase(project_id, "conversation", content, {
            "role": role,
            **(metadata or {})
        })
    
    async def store_decision(self, project_id: str, decision: str, rationale: str, components: List[str]):
        """Store a coding decision using Agno Memory"""
        memory = self._get_project_memory(project_id)
        
        content = f"Decision: {decision}\nRationale: {rationale}\nAffected Components: {', '.join(components)}"
        
        memory_item = MemoryItem(
            content=content,
            metadata={
                "type": "decision",
                "decision": decision,
                "rationale": rationale,
                "affected_components": components,
                "project_id": project_id
            },
            importance_score=0.9  # Decisions are very important
        )
        
        await memory.add(memory_item)
        
        # Store in Supabase
        await self._store_in_supabase(project_id, "decision", content, {
            "decision": decision,
            "rationale": rationale,
            "affected_components": components
        })
    
    async def store_pattern(self, project_id: str, pattern_name: str, pattern_code: str, usage_context: str):
        """Store a code pattern using Agno Memory"""
        memory = self._get_project_memory(project_id)
        
        content = f"Pattern: {pattern_name}\nCode: {pattern_code}\nContext: {usage_context}"
        
        memory_item = MemoryItem(
            content=content,
            metadata={
                "type": "pattern",
                "pattern_name": pattern_name,
                "usage_context": usage_context,
                "project_id": project_id
            },
            importance_score=0.8  # Patterns are important for reuse
        )
        
        await memory.add(memory_item)
        
        # Store in Supabase
        await self._store_in_supabase(project_id, "pattern", content, {
            "pattern_name": pattern_name,
            "usage_context": usage_context
        })
    
    async def store_preference(self, project_id: str, key: str, value: str):
        """Store a user preference using Agno Memory"""
        memory = self._get_project_memory(project_id)
        
        content = f"Preference: {key} = {value}"
        
        memory_item = MemoryItem(
            content=content,
            metadata={
                "type": "preference",
                "key": key,
                "value": value,
                "project_id": project_id
            },
            importance_score=0.7  # Preferences are moderately important
        )
        
        await memory.add(memory_item)
        
        # Store in Supabase
        await self._store_in_supabase(project_id, "preference", content, {
            "key": key,
            "value": value
        })
    
    async def get_project_memory(self, project_id: str, item_type: Optional[str] = None, limit: int = 50) -> List[Dict]:
        """Get memory items for a project using Agno Memory"""
        memory = self._get_project_memory(project_id)
        
        # Get recent memories from Agno
        recent_memories = await memory.get_recent(limit=limit)
        
        # Filter by type if specified
        if item_type:
            recent_memories = [
                mem for mem in recent_memories 
                if mem.metadata.get("type") == item_type
            ]
        
        # Convert to dict format
        return [
            {
                "id": mem.id,
                "content": mem.content,
                "metadata": mem.metadata,
                "importance_score": mem.importance_score,
                "created_at": mem.created_at
            }
            for mem in recent_memories
        ]
    
    async def search_memory(self, project_id: str, query: str, limit: int = 10) -> List[Dict]:
        """Search memory items using Agno's semantic search"""
        memory = self._get_project_memory(project_id)
        
        # Use Agno's semantic search
        search_results = await memory.search(
            query=query,
            limit=limit,
            similarity_threshold=0.6
        )
        
        # Convert to dict format
        return [
            {
                "id": mem.id,
                "content": mem.content,
                "metadata": mem.metadata,
                "importance_score": mem.importance_score,
                "similarity_score": mem.similarity_score,
                "created_at": mem.created_at
            }
            for mem in search_results
        ]
    
    async def get_relevant_context(self, project_id: str, query: str, context_type: Optional[str] = None) -> str:
        """Get relevant context for AI agents using Agno Memory"""
        memory = self._get_project_memory(project_id)
        
        # Search for relevant memories
        relevant_memories = await memory.search(
            query=query,
            limit=5,
            similarity_threshold=0.7
        )
        
        # Filter by context type if specified
        if context_type:
            relevant_memories = [
                mem for mem in relevant_memories 
                if mem.metadata.get("type") == context_type
            ]
        
        # Format context for AI
        context_parts = []
        for mem in relevant_memories:
            context_parts.append(f"[{mem.metadata.get('type', 'memory').upper()}] {mem.content}")
        
        return "\n\n".join(context_parts) if context_parts else ""
    
    async def _store_in_supabase(self, project_id: str, item_type: str, content: str, metadata: Dict):
        """Store memory item in Supabase for persistence"""
        memory_id = str(uuid.uuid4())
        
        memory_data = {
            "id": memory_id,
            "project_id": project_id,
            "item_type": item_type,
            "content": content,
            "metadata": metadata
        }
        
        self.supabase.table("memory_items").insert(memory_data).execute()
    
    async def load_project_memory_from_supabase(self, project_id: str):
        """Load existing memory items from Supabase into Agno Memory"""
        memory = self._get_project_memory(project_id)
        
        # Get existing memory items from Supabase
        response = self.supabase.table("memory_items")\
            .select("*")\
            .eq("project_id", project_id)\
            .order("created_at", desc=False)\
            .execute()
        
        # Load into Agno Memory
        for item in response.data:
            memory_item = MemoryItem(
                content=item["content"],
                metadata={
                    **item["metadata"],
                    "type": item["item_type"],
                    "project_id": project_id
                },
                importance_score=0.7  # Default importance
            )
            await memory.add(memory_item)
    
    async def clear_project_memory(self, project_id: str):
        """Clear all memory for a project"""
        if project_id in self._project_memories:
            memory = self._project_memories[project_id]
            await memory.clear()
            del self._project_memories[project_id]
        
        # Also clear from Supabase
        self.supabase.table("memory_items")\
            .delete()\
            .eq("project_id", project_id)\
            .execute()


# Singleton instance
memory_service = MemoryService()