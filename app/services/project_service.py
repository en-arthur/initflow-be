"""
Project-related business logic
"""
from typing import List, Optional
from app.database import get_supabase
from app.models import Project, User
import uuid


class ProjectService:
    def __init__(self):
        self.supabase = get_supabase()
    
    async def get_user_projects(self, user_id: str) -> List[dict]:
        """Get all projects for a user"""
        response = self.supabase.table("projects")\
            .select("*")\
            .eq("user_id", user_id)\
            .order("updated_at", desc=True)\
            .execute()
        
        return response.data
    
    async def get_project_by_id(self, project_id: str) -> Optional[dict]:
        """Get a project by ID"""
        response = self.supabase.table("projects")\
            .select("*")\
            .eq("id", project_id)\
            .execute()
        
        return response.data[0] if response.data else None
    
    async def create_project(self, user: User, name: str, description: Optional[str] = None) -> dict:
        """Create a new project with initial spec files"""
        project_id = str(uuid.uuid4())
        
        # Create project
        project_data = {
            "id": project_id,
            "user_id": user.id,
            "name": name,
            "description": description,
            "status": "draft",
            "tier": user.tier,
        }
        
        project_response = self.supabase.table("projects").insert(project_data).execute()
        
        if not project_response.data:
            raise Exception("Failed to create project")
        
        # Generate AI-powered spec files if description provided
        if description:
            await self._generate_ai_specs(project_id, user.id, name, description)
        else:
            await self._initialize_spec_files(project_id, user.id)
        
        return project_response.data[0]
    
    async def _generate_ai_specs(self, project_id: str, user_id: str, project_name: str, description: str):
        """Generate AI-powered specification files"""
        from app.services.spec_generator import spec_generator
        
        # Generate specs using AI
        specs = await spec_generator.generate_specs_from_prompt(description, project_name)
        
        # Create spec files with generated content
        for spec_type, content in specs.items():
            spec_id = str(uuid.uuid4())
            spec_data = {
                "id": spec_id,
                "project_id": project_id,
                "file_type": spec_type,
                "content": content,
                "version": 1,
                "created_by": user_id,
            }
            self.supabase.table("spec_files").insert(spec_data).execute()
    
    async def _initialize_spec_files(self, project_id: str, user_id: str):
        """Initialize the three spec files for a new project"""
        spec_templates = {
            "design": """# Design Specification

## Architecture Overview
Your app architecture will be defined here...

## UI/UX Design
- Color scheme
- Typography
- Component library
- Navigation structure

## Technical Stack
- React Native
- Expo
- State management
- API integration

## Responsive Design
- Mobile-first approach
- Screen size considerations
- Accessibility features
""",
            "requirements": """# Requirements Specification

## Project Overview
Brief description of your mobile application...

## User Stories

### Epic 1: Core Functionality
- As a user, I want to...
- As a user, I need to...

### Epic 2: Additional Features
- As a user, I want to...

## Acceptance Criteria
Each user story should have clear acceptance criteria...

## Non-Functional Requirements
- Performance requirements
- Security requirements
- Scalability requirements
""",
            "tasks": """# Implementation Tasks

## Phase 1: Setup and Foundation
- [ ] Set up project structure
- [ ] Configure navigation
- [ ] Implement basic UI components

## Phase 2: Core Features
- [ ] Implement main functionality
- [ ] Add data persistence
- [ ] Integrate APIs

## Phase 3: Polish and Testing
- [ ] Add error handling
- [ ] Implement testing
- [ ] Performance optimization

## Phase 4: Deployment
- [ ] Prepare for app stores
- [ ] Create app store assets
- [ ] Deploy to production
"""
        }
        
        for spec_type, content in spec_templates.items():
            spec_id = str(uuid.uuid4())
            spec_data = {
                "id": spec_id,
                "project_id": project_id,
                "file_type": spec_type,
                "content": content,
                "version": 1,
                "created_by": user_id,
            }
            self.supabase.table("spec_files").insert(spec_data).execute()
    
    async def update_project_status(self, project_id: str, status: str):
        """Update project status"""
        self.supabase.table("projects")\
            .update({"status": status})\
            .eq("id", project_id)\
            .execute()
    
    async def delete_project(self, project_id: str):
        """Delete a project and all related data"""
        # Supabase will handle cascade deletion due to foreign key constraints
        self.supabase.table("projects").delete().eq("id", project_id).execute()


# Singleton instance
project_service = ProjectService()