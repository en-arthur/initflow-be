from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# Enums
class UserTier(str, Enum):
    FREE = "free"
    PRO = "pro"
    PREMIUM = "premium"


class ProjectStatus(str, Enum):
    DRAFT = "draft"
    BUILDING = "building"
    READY = "ready"
    DEPLOYED = "deployed"
    ERROR = "error"


class SpecFileType(str, Enum):
    DESIGN = "design"
    REQUIREMENTS = "requirements"
    TASKS = "tasks"


class AgentType(str, Enum):
    DESIGN = "design"
    BACKEND = "backend"
    TESTING = "testing"


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class CodeChangeType(str, Enum):
    CREATE = "create"
    MODIFY = "modify"
    DELETE = "delete"


# Request Models
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    include_backend: bool = False


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None


class SpecFileUpdate(BaseModel):
    content: str


class SpecRollback(BaseModel):
    version_id: str


class FileUpdate(BaseModel):
    file_path: str
    content: str


class TaskCreate(BaseModel):
    description: str
    agent_type: AgentType


class ChangeApproval(BaseModel):
    approved: bool


class ChangeModification(BaseModel):
    feedback: str


class ChatMessage(BaseModel):
    message: str


# ComponentIntegration model disabled for now
# class ComponentIntegration(BaseModel):
#     component_id: str


class SubscriptionUpgrade(BaseModel):
    tier: UserTier


# Response Models
class User(BaseModel):
    id: str
    email: str
    name: str
    tier: UserTier
    credits_remaining: int
    created_at: datetime
    updated_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: User


class Project(BaseModel):
    id: str
    user_id: str
    name: str
    description: Optional[str]
    status: ProjectStatus
    tier: UserTier
    sandbox_id: Optional[str]
    created_at: datetime
    updated_at: datetime


class SpecFile(BaseModel):
    id: str
    project_id: str
    file_type: SpecFileType
    content: str
    version: int
    created_at: datetime
    created_by: str


class SpecVersion(BaseModel):
    id: str
    spec_file_id: str
    version: int
    content: str
    changes_summary: Optional[str]
    created_at: datetime
    created_by: str


class Task(BaseModel):
    id: str
    project_id: str
    agent_type: AgentType
    description: str
    status: TaskStatus
    input_context: Optional[Dict[str, Any]]
    output: Optional[Dict[str, Any]]
    created_at: datetime
    completed_at: Optional[datetime]


class CodeChange(BaseModel):
    id: str
    task_id: str
    file_path: str
    change_type: CodeChangeType
    diff: str
    agent_type: AgentType
    reasoning: Optional[str]
    approved: Optional[bool]
    created_at: datetime


class Sandbox(BaseModel):
    id: str
    project_id: str
    e2b_sandbox_id: str
    status: str
    preview_url: Optional[str]
    qr_code: Optional[str]
    cache_id: Optional[str]
    created_at: datetime
    last_active: datetime


class PreviewInfo(BaseModel):
    status: str
    preview_url: Optional[str]
    qr_code: Optional[str]


class ChatMessageResponse(BaseModel):
    id: str
    role: str
    content: str
    timestamp: datetime
    attachments: Optional[List[Dict[str, Any]]]


# MarketplaceComponent model disabled for now
# class MarketplaceComponent(BaseModel):
#     id: str
#     name: str
#     description: str
#     category: str
#     tags: List[str]
#     preview_url: Optional[str]
#     spec_template: Dict[str, Any]
#     code_template: Dict[str, Any]
#     dependencies: List[str]
#     downloads: int
#     rating: float
#     created_at: datetime


class BuildJob(BaseModel):
    id: str
    project_id: str
    platform: str
    status: str
    build_url: Optional[str]
    error_message: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]


class Subscription(BaseModel):
    tier: UserTier
    credits_remaining: int
    projects_count: int
    projects_limit: Optional[int]
