"""
E2B Sandbox management service
"""
from typing import Optional, Dict, Any
from app.database import get_supabase
import uuid


class SandboxService:
    """Service for managing E2B sandboxes"""
    
    def __init__(self):
        self.supabase = get_supabase()
    
    async def create_sandbox(self, project_id: str) -> Dict[str, Any]:
        """Create a new E2B sandbox for a project"""
        # In production, this would use the E2B SDK
        # For now, create a mock sandbox entry
        
        sandbox_id = str(uuid.uuid4())
        e2b_sandbox_id = f"sb_{uuid.uuid4().hex[:8]}"
        
        sandbox_data = {
            "id": sandbox_id,
            "project_id": project_id,
            "e2b_sandbox_id": e2b_sandbox_id,
            "status": "initializing",
            "preview_url": None,
            "qr_code": None,
            "cache_id": None,
        }
        
        response = self.supabase.table("sandboxes").insert(sandbox_data).execute()
        
        if response.data:
            # Simulate sandbox initialization
            await self._initialize_sandbox(sandbox_id, e2b_sandbox_id)
            return response.data[0]
        
        raise Exception("Failed to create sandbox")
    
    async def _initialize_sandbox(self, sandbox_id: str, e2b_sandbox_id: str):
        """Initialize the sandbox with Expo template"""
        # Simulate initialization process
        import asyncio
        await asyncio.sleep(1)  # Simulate setup time
        
        # Update sandbox status
        preview_url = f"https://expo.dev/@preview/{e2b_sandbox_id}"
        qr_code = self._generate_qr_code(preview_url)
        
        self.supabase.table("sandboxes")\
            .update({
                "status": "ready",
                "preview_url": preview_url,
                "qr_code": qr_code,
                "last_active": "now()"
            })\
            .eq("id", sandbox_id)\
            .execute()
    
    def _generate_qr_code(self, url: str) -> str:
        """Generate QR code for the preview URL"""
        # In production, use qrcode library
        # For now, return a placeholder data URL
        return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    
    async def get_sandbox(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Get sandbox for a project"""
        response = self.supabase.table("sandboxes")\
            .select("*")\
            .eq("project_id", project_id)\
            .order("created_at", desc=True)\
            .limit(1)\
            .execute()
        
        return response.data[0] if response.data else None
    
    async def update_sandbox_files(self, sandbox_id: str, files: Dict[str, str]):
        """Update files in the sandbox"""
        # In production, this would sync files to E2B
        # For now, just update the last_active timestamp
        self.supabase.table("sandboxes")\
            .update({"last_active": "now()"})\
            .eq("id", sandbox_id)\
            .execute()
        
        return {"message": "Files updated successfully"}
    
    async def get_preview_info(self, project_id: str) -> Dict[str, Any]:
        """Get preview information for a project"""
        sandbox = await self.get_sandbox(project_id)
        
        if not sandbox:
            # Create sandbox if it doesn't exist
            sandbox = await self.create_sandbox(project_id)
        
        return {
            "status": sandbox["status"],
            "preview_url": sandbox["preview_url"],
            "qr_code": sandbox["qr_code"]
        }
    
    async def cache_sandbox_state(self, sandbox_id: str) -> str:
        """Cache the current sandbox state"""
        cache_id = f"cache_{uuid.uuid4().hex[:8]}"
        
        # In production, this would snapshot the E2B sandbox
        self.supabase.table("sandboxes")\
            .update({"cache_id": cache_id})\
            .eq("id", sandbox_id)\
            .execute()
        
        return cache_id
    
    async def restore_sandbox(self, project_id: str, cache_id: str) -> Dict[str, Any]:
        """Restore sandbox from cached state"""
        # In production, this would restore from E2B cache
        # For now, just create a new sandbox
        return await self.create_sandbox(project_id)


# Singleton instance
sandbox_service = SandboxService()