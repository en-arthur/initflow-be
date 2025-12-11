from fastapi import APIRouter, Depends
from app.models import User
from app.auth import get_current_user
from app.database import get_supabase

router = APIRouter()


@router.get("/projects/{project_id}/summary")
async def get_project_summary(
    project_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get project summary with stats"""
    supabase = get_supabase()
    
    # Get project info
    project = supabase.table("projects")\
        .select("*")\
        .eq("id", project_id)\
        .eq("user_id", current_user.id)\
        .execute()
    
    if not project.data:
        return {"error": "Project not found"}
    
    # Get spec files count
    specs = supabase.table("spec_files")\
        .select("file_type", count="exact")\
        .eq("project_id", project_id)\
        .execute()
    
    # Get tasks count
    tasks = supabase.table("tasks")\
        .select("status", count="exact")\
        .eq("project_id", project_id)\
        .execute()
    
    # Get pending changes count
    pending_changes = supabase.table("code_changes")\
        .select("id", count="exact")\
        .eq("tasks.project_id", project_id)\
        .is_("approved", "null")\
        .execute()
    
    # Get approved changes count
    approved_changes = supabase.table("code_changes")\
        .select("id", count="exact")\
        .eq("tasks.project_id", project_id)\
        .eq("approved", True)\
        .execute()
    
    return {
        "project": project.data[0],
        "stats": {
            "spec_files": specs.count or 0,
            "total_tasks": tasks.count or 0,
            "pending_changes": pending_changes.count or 0,
            "approved_changes": approved_changes.count or 0,
        }
    }


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Spec-Driven AI App Builder API",
        "version": "1.0.0"
    }