from fastapi import APIRouter
from authenticate_service.api.v1.endpoints import auth_router

api_router = APIRouter()

# Mount authentication endpoints under /auth with tag "Authentication"
api_router.include_router(
    auth_router.router,
    prefix="/auth",
    tags=["Authentication"],
)

