from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.models import Task, TaskCreate, CodeChange, ChangeModification, User
from app.auth import get_current_user
from app.database import get_supabase
import uuid

router = APIRouter()


@router.post("/tasks", response_model=Task)
async def submit_task(
    project_id: str,
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user)
):
    """Submit a task to an agent"""
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
    
    # Create task
    import uuid
    task_id = str(uuid.uuid4())
    task_data_dict = {
        "id": task_id,
        "project_id": project_id,
        "agent_type": task_data.agent_type,
        "description": task_data.description,
        "status": "pending",
        "input_context": {"user_request": task_data.description},
    }
    
    task_response = supabase.table("tasks").insert(task_data_dict).execute()
    
    # Process agent task with AI
    await process_agent_task(task_id, task_data.agent_type, task_data.description, current_user)
    
    return Task(**task_response.data[0])


async def process_agent_task(task_id: str, agent_type: str, description: str, user: User):
    """Process a task with the appropriate agent using AI"""
    from app.services.ai_service import ai_service
    supabase = get_supabase()
    
    # Get project context
    task_response = supabase.table("tasks").select("project_id").eq("id", task_id).execute()
    project_id = task_response.data[0]["project_id"] if task_response.data else None
    
    project_context = {}
    if project_id:
        # Get project specs for context
        specs = supabase.table("spec_files").select("file_type, content").eq("project_id", project_id).execute()
        project_context = {spec["file_type"]: spec["content"][:1000] for spec in specs.data}
    
    # Generate code using AI service
    code_result = await ai_service.generate_code(user, description, agent_type, project_context)
    
    # Create code changes for each generated file
    for file_path, file_content in code_result["files"].items():
        change_id = str(uuid.uuid4())
        
        # Create diff format
        diff = "\n".join([f"+ {line}" for line in file_content.split("\n")])
        
        change_data = {
            "id": change_id,
            "task_id": task_id,
            "file_path": file_path,
            "change_type": "create",
            "diff": diff,
            "agent_type": agent_type,
            "reasoning": code_result["reasoning"],
            "approved": None,  # Pending approval
        }
        
        supabase.table("code_changes").insert(change_data).execute()
    
    # Update task status
    supabase.table("tasks")\
        .update({
            "status": "completed",
            "output": {"generated_files": list(code_result["files"].keys())},
            "completed_at": "now()"
        })\
        .eq("id", task_id)\
        .execute()


@router.get("/changes/pending", response_model=List[CodeChange])
async def get_pending_changes(
    project_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get pending code changes"""
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
    
    # Get pending changes (approved = null means pending)
    changes_response = supabase.table("code_changes")\
        .select("*, tasks!inner(project_id)")\
        .eq("tasks.project_id", project_id)\
        .is_("approved", "null")\
        .order("created_at", desc=True)\
        .execute()
    
    return [CodeChange(**change) for change in changes_response.data]


@router.post("/changes/{change_id}/approve")
async def approve_change(
    project_id: str,
    change_id: str,
    current_user: User = Depends(get_current_user)
):
    """Approve a code change"""
    supabase = get_supabase()
    
    # Verify change exists and belongs to user's project
    change_response = supabase.table("code_changes")\
        .select("*, tasks!inner(project_id, projects!inner(user_id))")\
        .eq("id", change_id)\
        .eq("tasks.project_id", project_id)\
        .execute()
    
    if not change_response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Code change not found"
        )
    
    change = change_response.data[0]
    if change["tasks"]["projects"]["user_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Update change as approved
    supabase.table("code_changes")\
        .update({"approved": True})\
        .eq("id", change_id)\
        .execute()
    
    # TODO: Apply the change to the actual codebase/sandbox
    
    return {"message": "Change approved successfully"}


@router.post("/changes/{change_id}/reject")
async def reject_change(
    project_id: str,
    change_id: str,
    current_user: User = Depends(get_current_user)
):
    """Reject a code change"""
    supabase = get_supabase()
    
    # Verify change exists and belongs to user's project
    change_response = supabase.table("code_changes")\
        .select("*, tasks!inner(project_id, projects!inner(user_id))")\
        .eq("id", change_id)\
        .eq("tasks.project_id", project_id)\
        .execute()
    
    if not change_response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Code change not found"
        )
    
    change = change_response.data[0]
    if change["tasks"]["projects"]["user_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Update change as rejected
    supabase.table("code_changes")\
        .update({"approved": False})\
        .eq("id", change_id)\
        .execute()
    
    return {"message": "Change rejected successfully"}


@router.post("/changes/{change_id}/modify")
async def request_modification(
    project_id: str,
    change_id: str,
    modification: ChangeModification,
    current_user: User = Depends(get_current_user)
):
    """Request modification to a code change"""
    supabase = get_supabase()
    
    # Verify change exists and belongs to user's project
    change_response = supabase.table("code_changes")\
        .select("*, tasks!inner(project_id, projects!inner(user_id))")\
        .eq("id", change_id)\
        .eq("tasks.project_id", project_id)\
        .execute()
    
    if not change_response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Code change not found"
        )
    
    change = change_response.data[0]
    if change["tasks"]["projects"]["user_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Create new task for modification
    task_id = str(uuid.uuid4())
    task_data = {
        "id": task_id,
        "project_id": project_id,
        "agent_type": change["agent_type"],
        "description": f"Modify previous change: {modification.feedback}",
        "status": "pending",
        "input_context": {
            "modification_request": modification.feedback,
            "original_change_id": change_id,
            "original_file": change["file_path"]
        },
    }
    
    supabase.table("tasks").insert(task_data).execute()
    
    # Mark original change as rejected
    supabase.table("code_changes")\
        .update({"approved": False})\
        .eq("id", change_id)\
        .execute()
    
    # Process the modification request
    await process_modification_request(task_id, change, modification.feedback)
    
    return {"message": "Modification request submitted successfully"}


@router.get("/sandbox")
async def get_sandbox(
    project_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get sandbox information"""
    from app.services.sandbox_service import sandbox_service
    
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
    
    sandbox = await sandbox_service.get_sandbox(project_id)
    
    if not sandbox:
        # Create sandbox if it doesn't exist
        sandbox = await sandbox_service.create_sandbox(project_id)
    
    return sandbox


@router.get("/preview")
async def get_preview(
    project_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get preview information"""
    from app.services.sandbox_service import sandbox_service
    
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
    
    # Get preview info from sandbox service
    preview_info = await sandbox_service.get_preview_info(project_id)
    return preview_info


@router.post("/build")
async def create_build(
    project_id: str,
    platform: str,
    current_user: User = Depends(get_current_user)
):
    """Create a build for deployment"""
    from app.services.deployment_service import deployment_service
    
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
    
    if platform not in ["ios", "android", "both"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Platform must be 'ios', 'android', or 'both'"
        )
    
    # Create build job
    build_job = await deployment_service.create_build_job(project_id, platform)
    return build_job


@router.get("/builds/{build_id}")
async def get_build_status(
    project_id: str,
    build_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get build status"""
    from app.services.deployment_service import deployment_service
    
    build_status = await deployment_service.get_build_status(build_id)
    
    if not build_status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Build not found"
        )
    
    return build_status


@router.get("/deployment-guide/{platform}")
async def get_deployment_guide(
    project_id: str,
    platform: str,
    current_user: User = Depends(get_current_user)
):
    """Get deployment guide for platform"""
    from app.services.deployment_service import deployment_service
    
    guide = await deployment_service.get_deployment_guide(platform)
    return guide


async def process_modification_request(task_id: str, original_change: dict, feedback: str):
    """Process a modification request and create a new code change"""
    supabase = get_supabase()
    
    # Generate modified code based on feedback
    change_id = str(uuid.uuid4())
    
    # Create a modified version of the original change
    modified_diff = f"""# Modified based on feedback: {feedback}
{original_change['diff']}
+ // Additional modifications based on user feedback
+ // {feedback}"""
    
    change_data = {
        "id": change_id,
        "task_id": task_id,
        "file_path": original_change["file_path"],
        "change_type": "modify",
        "diff": modified_diff,
        "agent_type": original_change["agent_type"],
        "reasoning": f"Modified based on user feedback: {feedback}",
        "approved": None,  # Pending approval
    }
    
    supabase.table("code_changes").insert(change_data).execute()
    
    # Update task status
    supabase.table("tasks")\
        .update({
            "status": "completed",
            "output": {"modification_applied": True, "feedback": feedback},
            "completed_at": "now()"
        })\
        .eq("id", task_id)\
        .execute()
