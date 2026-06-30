from fastapi import APIRouter
from app.api import auth, users, documents, schemes, applications, agents, audit

api_router = APIRouter()

# Include all sub-routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])
api_router.include_router(schemes.router, prefix="/schemes", tags=["Schemes"])
api_router.include_router(applications.router, prefix="/applications", tags=["Applications"])
api_router.include_router(agents.router, prefix="/agents", tags=["Agents"])
api_router.include_router(audit.router, prefix="/audit", tags=["Audit"])
