import json
import ast
from fastapi import Request
from authenticate_service.repositories.auth_repository import AuthRepository
from authenticate_service.schemas.auth_schema import (
    AuthRequest,
    AuthenticateResponse,
    AuthorizeResponse,
    LogoutRequest,
    LogoutResponse,
)


class AuthService:
    def __init__(self):
        self.repo = AuthRepository()

    async def authenticate(self, auth_request: AuthRequest) -> AuthenticateResponse:
        auth_obj = self.repo.authenticate(auth_request)
        return auth_obj

    async def authorize(self, authorize_request: AuthRequest, req: Request) -> AuthorizeResponse:
        authorize_obj = self.repo.authorize(authorize_request, req)
        return authorize_obj

    async def logout(self, request: LogoutRequest):
        try:
            # 1) Get admin token
            try:
                admin_token = self.repo.get_admin_token()
            except Exception as e:
                return LogoutResponse(message=f"Failed to get admin token: {e}")
            print("in logout service")
            # 2) Keycloak logout (repo resolves id -> email -> UUID)
            keycloak_success = self.repo.logout_keycloak(request.id, admin_token)

            # 3) Mark user offline in DB (independent step)
            db_success = self.repo.set_user_offline(request.id)

            if keycloak_success and db_success:
                return LogoutResponse(message="User logged out from Keycloak and marked offline")
            elif keycloak_success and not db_success:
                return LogoutResponse(message="Keycloak logout OK, but failed to mark user offline in DB")
            elif not keycloak_success and db_success:
                return LogoutResponse(message="Marked user offline in DB, but Keycloak logout failed")
            else:
                return LogoutResponse(message="Keycloak logout and DB update both failed")
        except Exception as e:
            print(f"[SERVICE LOGOUT ERROR] {e}")
            return LogoutResponse(message="Unexpected error during logout")

    async def forgot_password(self, request: LogoutRequest) -> LogoutResponse:
        """
        Sends a password reset email via Keycloak (execute-actions-email: UPDATE_PASSWORD).
        """
        try:
            try:
                admin_token = self.repo.get_admin_token()
            except Exception as e:
                return LogoutResponse(message=f"Failed to get admin token: {e}")

            success = self.repo.reset_user_password(id=request.id, admin_token=admin_token)
            if success:
                return LogoutResponse(message="Forgot password email sent successfully")
            return LogoutResponse(message="Failed to send reset password email")
        except Exception as e:
            print(f"[SERVICE FORGOT_PWD ERROR] {e}")
            return LogoutResponse(message="Internal server error during password reset")

    async def reset_password(self, request: LogoutRequest) -> LogoutResponse:
        """
        Same behavior as forgot_password (triggers reset email).
        """
        try:
            try:
                admin_token = self.repo.get_admin_token()
            except Exception as e:
                return LogoutResponse(message=f"Failed to get admin token: {e}")

            success = self.repo.reset_user_password(id=request.id, admin_token=admin_token)
            if success:
                return LogoutResponse(message="Reset password email sent successfully")
            return LogoutResponse(message="Failed to send reset password email")
        except Exception as e:
            print(f"[SERVICE RESET_PWD ERROR] {e}")
            return LogoutResponse(message="Internal server error during password reset")

    async def change_password(self, request: LogoutRequest):
        try:
            try:
                admin_token = self.repo.get_admin_token()
            except Exception as e:
                return {"message": f"Failed to get admin token: {e}"}

            success = self.repo.reset_user_password(id=request.id, admin_token=admin_token)
            if success:
                return {"message": "Change password email sent successfully"}
            else:
                return {"message": "Failed to send reset password email"}
        except Exception as e:
            print(f"[SERVICE CHANGE_PWD ERROR] {e}")
            return {"message": "Internal server error during password reset"}

    async def refresh_token(self, refresh_token: str):
        return await self.repo.refresh_token(refresh_token)
