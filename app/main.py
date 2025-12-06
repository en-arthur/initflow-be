from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import auth, projects, specs, files, agents, chat, marketplace, subscription

app = FastAPI(
    title="Spec-Driven AI App Builder API",
    description="Backend API for the Spec-Driven AI App Builder platform",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(specs.router, prefix="/api/projects/{project_id}/specs", tags=["Specifications"])
app.include_router(files.router, prefix="/api/projects/{project_id}/files", tags=["Files"])
app.include_router(agents.router, prefix="/api/projects/{project_id}", tags=["Agents"])
app.include_router(chat.router, prefix="/api/projects/{project_id}/chat", tags=["Chat"])
app.include_router(marketplace.router, prefix="/api/marketplace", tags=["Marketplace"])
app.include_router(subscription.router, prefix="/api/subscription", tags=["Subscription"])


@app.get("/")
async def root():
    return {
        "message": "Spec-Driven AI App Builder API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
