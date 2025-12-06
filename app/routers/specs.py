from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.models import SpecFile, SpecVersion, SpecFileUpdate, SpecRollback, User
from app.auth import get_current_user
from app.database import get_supabase
import uuid

router = APIRouter()


@router.get("/{file_type}", response_model=SpecFile)
async def get_spec_file(
    project_id: str,
    file_type: str,
    current_user: User = Depends(get_current_user)
):
    """Get a spec file"""
    supabase = get_supabase()
    
    response = supabase.table("spec_files")\
        .select("*")\
        .eq("project_id", project_id)\
        .eq("file_type", file_type)\
        .order("version", desc=True)\
        .limit(1)\
        .execute()
    
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Spec file not found"
        )
    
    return SpecFile(**response.data[0])


@router.put("/{file_type}", response_model=SpecFile)
async def update_spec_file(
    project_id: str,
    file_type: str,
    spec_data: SpecFileUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update a spec file (creates new version)"""
    supabase = get_supabase()
    
    # Get current spec file
    current_response = supabase.table("spec_files")\
        .select("*")\
        .eq("project_id", project_id)\
        .eq("file_type", file_type)\
        .order("version", desc=True)\
        .limit(1)\
        .execute()
    
    if not current_response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Spec file not found"
        )
    
    current_spec = current_response.data[0]
    
    # Save current version to history
    import uuid
    version_id = str(uuid.uuid4())
    version_data = {
        "id": version_id,
        "spec_file_id": current_spec["id"],
        "version": current_spec["version"],
        "content": current_spec["content"],
        "changes_summary": "Updated via editor",
        "created_by": current_user.id,
    }
    supabase.table("spec_versions").insert(version_data).execute()
    
    # Update spec file with new content and increment version
    new_version = current_spec["version"] + 1
    update_data = {
        "content": spec_data.content,
        "version": new_version,
    }
    
    response = supabase.table("spec_files")\
        .update(update_data)\
        .eq("id", current_spec["id"])\
        .execute()
    
    return SpecFile(**response.data[0])


@router.get("/{file_type}/versions", response_model=List[SpecVersion])
async def get_spec_versions(
    project_id: str,
    file_type: str,
    current_user: User = Depends(get_current_user)
):
    """Get version history for a spec file"""
    supabase = get_supabase()
    
    # Get spec file id
    spec_response = supabase.table("spec_files")\
        .select("id")\
        .eq("project_id", project_id)\
        .eq("file_type", file_type)\
        .limit(1)\
        .execute()
    
    if not spec_response.data:
        return []
    
    spec_file_id = spec_response.data[0]["id"]
    
    # Get versions
    versions_response = supabase.table("spec_versions")\
        .select("*")\
        .eq("spec_file_id", spec_file_id)\
        .order("version", desc=True)\
        .execute()
    
    return [SpecVersion(**version) for version in versions_response.data]


@router.post("/{file_type}/rollback", response_model=SpecFile)
async def rollback_spec(
    project_id: str,
    file_type: str,
    rollback_data: SpecRollback,
    current_user: User = Depends(get_current_user)
):
    """Rollback to a previous version"""
    supabase = get_supabase()
    
    # Get the version to rollback to
    version_response = supabase.table("spec_versions")\
        .select("*")\
        .eq("id", rollback_data.version_id)\
        .execute()
    
    if not version_response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Version not found"
        )
    
    version = version_response.data[0]
    
    # Get current spec file
    spec_response = supabase.table("spec_files")\
        .select("*")\
        .eq("id", version["spec_file_id"])\
        .execute()
    
    if not spec_response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Spec file not found"
        )
    
    current_spec = spec_response.data[0]
    
    # Save current state to history before rollback
    import uuid
    history_id = str(uuid.uuid4())
    history_data = {
        "id": history_id,
        "spec_file_id": current_spec["id"],
        "version": current_spec["version"],
        "content": current_spec["content"],
        "changes_summary": f"Before rollback to version {version['version']}",
        "created_by": current_user.id,
    }
    supabase.table("spec_versions").insert(history_data).execute()
    
    # Update spec file with rolled back content
    new_version = current_spec["version"] + 1
    update_data = {
        "content": version["content"],
        "version": new_version,
    }
    
    response = supabase.table("spec_files")\
        .update(update_data)\
        .eq("id", current_spec["id"])\
        .execute()
    
    return SpecFile(**response.data[0])
