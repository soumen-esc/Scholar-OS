from app.core.config import settings
from fastapi import FastAPI
from app.database.database import Base, engine
from app.models.user import User
from app.routers.auth import router as auth_router
from app.routers.project import router as project_router
from app.routers.paper import router as paper_router
from app.models.project import Project
from app.models.paper import Paper
from app.models.notification import Notification
from app.routers.notification import router as notification_router

Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "Authentication",
        "description": "User registration, login, and authentication endpoints.",
    },
    {
        "name": "Projects",
        "description": "Create and manage research projects.",
    },
    {
        "name": "Papers",
        "description": "Create and manage research paper metadata.",
    },
    {
        "name": "Notifications",
        "description": "Create, retrieve, update, and delete user notifications.",
    },
]


app = FastAPI(
    title="ResearchOS Backend API",
    description=(
        "Backend REST API for the ResearchOS AI Research Assistant Platform. "
        "Provides authentication, project management, paper metadata management, "
        "and notification services."
    ),
    version="1.0.0",
    openapi_tags=tags_metadata
)

app.include_router(auth_router)
app.include_router(project_router)
app.include_router(paper_router)
app.include_router(notification_router)

@app.get("/")
def root():
    return {
        "project": "ResearchOS",
        "status": "Backend Running",
        "version": "1.0.0"
    }
@app.get("/about")
def about():
    return {
        "developer": "Soumen",
        "project": "ResearchOS",
        "backend": "FastAPI"
    }
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }