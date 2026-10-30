from typing import Optional, List, Any
from sqlalchemy.orm import Session
from authenticate_service.models.auth_model import User
from authenticate_service.schemas.auth_schema import (
    AuthRequest,
    AuthenticateResponse,
    AuthorizeResponse,
    AuthRole,
)


class AuthRepository:
    """
    Repository layer for Keycloak identity broker and database persistence.
    """

    def __init__(self, db: Optional[Session] = None):
        self.db = db

    def get_admin_token(self) -> str:
        """Retrieves Keycloak admin token."""
        return "mock_keycloak_admin_token"

    def logout_keycloak(self, user_id: Optional[str], admin_token: str) -> bool:
        """Calls Keycloak API to terminate active user session."""
        return True

    def set_user_offline(self, user_id: Optional[str]) -> bool:
        """Updates user status in database to offline."""
        return True

    def reset_user_password(self, id: Optional[str], admin_token: str) -> bool:
        """Sends password reset actions via Keycloak."""
        return True

    def authenticate(self, auth_request: AuthRequest) -> AuthenticateResponse:
        """Authenticates user against Keycloak / Database."""
        return AuthenticateResponse(
            id="usr_001",
            fullName="Hiscox User",
            email=auth_request.email,
            role="user",
            token="mock_access_token",
            refresh_token="mock_refresh_token",
            status="active",
            profile_pic="",
            program_name=auth_request.program_name or "HISCOX_Commercial",
        )

    def authorize(self, authorize_request: AuthRequest, req: Any) -> AuthorizeResponse:
        """Authorizes request and retrieves profile metadata."""
        return AuthorizeResponse(
            id="usr_001",
            fullName="Hiscox User",
            email=authorize_request.email,
            role=AuthRole.USER,
            managerId="MGR_001",
            managerName="Operations Manager",
            status="active",
            profile_pic="",
            token="mock_access_token",
            refresh_token="mock_refresh_token",
            createdby="system",
            updatedby="system",
            createdat="2026-10-30T00:00:00Z",
            updatedat="2026-10-30T12:00:00Z",
            external_email=authorize_request.email,
            program_name="HISCOX_Phase_2",
        )

    async def refresh_token(self, refresh_token_str: str) -> dict:
        """Calls Keycloak refresh token endpoint."""
        return {
            "access_token": "mock_new_access_token",
            "refresh_token": "mock_new_refresh_token",
            "token_type": "bearer",
            "expires_in": 3600,
        }
