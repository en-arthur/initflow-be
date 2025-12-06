from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models import Task, TaskCreate, CodeChange, ChangeModification, User
from app.auth import get_current_user

router = APIRouter()


@router.post("/tasks", response_model=Task)
async def submit_task(
    project_id: str,
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user)
):
    """Submit a task to an agent"""
    # TODO: Implement agent task submission
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/changes/pending", response_model=List[CodeChange])
async def get_pending_changes(
    project_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get pending code changes"""
    # TODO: Implement pending changes retrieval
    return []


@router.post("/changes/{change_id}/approve")
async def approve_change(
    project_id: str,
    change_id: str,
    current_user: User = Depends(get_current_user)
):
    """Approve a code change"""
    # TODO: Implement change approval
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.post("/changes/{change_id}/reject")
async def reject_change(
    project_id: str,
    change_id: str,
    current_user: User = Depends(get_current_user)
):
    """Reject a code change"""
    # TODO: Implement change rejection
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.post("/changes/{change_id}/modify")
async def request_modification(
    project_id: str,
    change_id: str,
    modification: ChangeModification,
    current_user: User = Depends(get_current_user)
):
    """Request modification to a code change"""
    # TODO: Implement modification request
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/sandbox")
async def get_sandbox(
    project_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get sandbox information"""
    # TODO: Implement sandbox info retrieval
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/preview")
async def get_preview(
    project_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get preview information"""
    # TODO: Implement preview info retrieval
    return {
        "status": "building",
        "preview_url": None,
        "qr_code": None
    }
