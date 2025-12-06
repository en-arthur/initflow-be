from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.models import Project, ProjectCreate, ProjectUpdate, User
from app.auth import get_current_user, check_project_access, check_tier_limits
from app.database import get_supabase
import uuid

router = APIRouter()


@router.get("", response_model=List[Project])
async def get_projects(current_user: User = Depends(get_current_user)):
    """Get all projects for the current user"""
    supabase = get_supabase()
    
    response = supabase.table("projects")\
        .select("*")\
        .eq("user_id", current_user.id)\
        .order("updated_at", desc=True)\
        .execute()
    
    return [Project(**project) for project in response.data]


@router.get("/{project_id}", response_model=Project)
async def get_project(
    project_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get a specific project"""
    supabase = get_supabase()
    
    response = supabase.table("projects")\
        .select("*")\
        .eq("id", project_id)\
        .execute()
    
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    project = response.data[0]
    check_project_access(current_user, project["user_id"])
    
    return Project(**project)


@router.post("", response_model=Project, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new project"""
    supabase = get_supabase()
    
    # Check tier limits
    projects_response = supabase.table("projects")\
        .select("id")\
        .eq("user_id", current_user.id)\
        .execute()
    
    check_tier_limits(current_user, len(projects_response.data))
    
    # Create project
    project_id = str(uuid.uuid4())
    new_project = {
        "id": project_id,
        "user_id": current_user.id,
        "name": project_data.name,
        "description": project_data.description,
        "status": "draft",
        "tier": current_user.tier,
    }
    
    response = supabase.table("projects").insert(new_project).execute()
    
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create project"
        )
    
    # Initialize spec files
    spec_types = ["design", "requirements", "tasks"]
    for spec_type in spec_types:
        spec_id = str(uuid.uuid4())
        spec_data = {
            "id": spec_id,
            "project_id": project_id,
            "file_type": spec_type,
            "content": f"# {spec_type.capitalize()}\n\nYour {spec_type} will be generated here...",
            "version": 1,
            "created_by": current_user.id,
        }
        supabase.table("spec_files").insert(spec_data).execute()
    
    return Project(**response.data[0])


@router.put("/{project_id}", response_model=Project)
async def update_project(
    project_id: str,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update a project"""
    supabase = get_supabase()
    
    # Check project exists and user has access
    project_response = supabase.table("projects")\
        .select("*")\
        .eq("id", project_id)\
        .execute()
    
    if not project_response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    check_project_access(current_user, project_response.data[0]["user_id"])
    
    # Update project
    update_data = project_data.dict(exclude_unset=True)
    if not update_data:
        return Project(**project_response.data[0])
    
    response = supabase.table("projects")\
        .update(update_data)\
        .eq("id", project_id)\
        .execute()
    
    return Project(**response.data[0])


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete a project"""
    supabase = get_supabase()
    
    # Check project exists and user has access
    project_response = supabase.table("projects")\
        .select("user_id")\
        .eq("id", project_id)\
        .execute()
    
    if not project_response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    check_project_access(current_user, project_response.data[0]["user_id"])
    
    # Delete project (cascade will handle related records)
    supabase.table("projects").delete().eq("id", project_id).execute()
    
    return None
