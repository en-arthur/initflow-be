from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from app.models import FileUpdate, User
from app.auth import get_current_user

router = APIRouter()


@router.get("", response_model=Dict[str, Any])
async def get_project_files(
    project_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get all project files"""
    # TODO: Implement file tree retrieval from sandbox
    return {}


@router.put("", response_model=Dict[str, str])
async def update_file(
    project_id: str,
    file_data: FileUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update a project file"""
    # TODO: Implement file update in sandbox
    raise HTTPException(status_code=501, detail="Not implemented yet")
