from fastapi import APIRouter, Depends, Request, HTTPException, status
from authenticate_service.services.auth_service import AuthService
from authenticate_service.schemas.auth_schema import (
    AuthRequest,
    AuthResponse,
    AuthenticateResponse,
    AuthorizeResponse,
    APIResponse,
    LogoutRequest,
    RefreshTokenRequest,
)

router = APIRouter()

COMMON_404_RESPONSE = {
    404: {
        "description": "Resource or metadata not found",
        "content": {"application/json": {"example": {"detail": "Metadata data not found"}}},
    }
}
COMMON_500_RESPONSE = {
    500: {
        "description": "Internal server error",
        "content": {"application/json": {"example": {"detail": "Internal server error occurred"}}},
    }
}


@router.post(
    "/authenticate",
    response_model=AuthenticateResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate User Request",
    description="Validates user credentials against coaching metadata and returns the user authentication context.",
    responses={
        200: {"description": "User authentication successful", "model": AuthenticateResponse},
        **COMMON_404_RESPONSE,
        **COMMON_500_RESPONSE,
    },
)
async def authenticate(
    auth_request: AuthRequest,
    service: AuthService = Depends(),
):
    try:
        auth_data = await service.authenticate(auth_request)
        if auth_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Metadata data not found",
            )
        return auth_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post(
    "/authorize",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Authorize User Request",
    description="Authorizes client request, verifies permissions, and returns authorization payload.",
    responses={
        200: {"description": "Authorization successful", "model": APIResponse},
        **COMMON_404_RESPONSE,
        **COMMON_500_RESPONSE,
    },
)
async def authorize(
    authorize_request: AuthRequest,
    req: Request,
    service: AuthService = Depends(),
):
    try:
        auth_data = await service.authorize(authorize_request, req)
        if auth_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Metadata data not found",
            )
        return {"status": "success", "code": 200, "data": auth_data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post(
    "/logout",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Logout User",
    description="Invalidates active user session and auth tokens.",
    responses={
        200: {"description": "User logged out successfully", "model": APIResponse},
        404: {
            "description": "Logout data not found",
            "content": {"application/json": {"example": {"detail": "Logout data not found"}}},
        },
        **COMMON_500_RESPONSE,
    },
)
async def logout(
    request: LogoutRequest,
    service: AuthService = Depends(),
):
    try:
        logout_data = await service.logout(request)
        if logout_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Logout data not found",
            )
        return {"status": "success", "code": 200, "data": logout_data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.put(
    "/forgot_password",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Forgot Password",
    description="Initiates password recovery process by generating a reset token.",
    responses={
        200: {"description": "Password reset initiated successfully", "model": APIResponse},
        404: {
            "description": "Result of forgot password data not found",
            "content": {"application/json": {"example": {"detail": "Result of forgot password data not found"}}},
        },
        **COMMON_500_RESPONSE,
    },
)
async def forgot_password(
    request: LogoutRequest,
    service: AuthService = Depends(),
):
    try:
        result = await service.forgot_password(request)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Result of forgot password data not found",
            )
        return {"status": "success", "code": 200, "data": result}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.put(
    "/reset_password",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Reset Password",
    description="Resets the user's password using the provided reset token and credentials.",
    responses={
        200: {"description": "Password reset successfully", "model": APIResponse},
        404: {
            "description": "Result of reset password data not found",
            "content": {"application/json": {"example": {"detail": "Result of reset password data not found"}}},
        },
        **COMMON_500_RESPONSE,
    },
)
async def reset_password(
    request: LogoutRequest,
    service: AuthService = Depends(),
):
    try:
        result = await service.reset_password(request)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Result of reset password data not found",
            )
        return {"status": "success", "code": 200, "data": result}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.put(
    "/change_password",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Change Password",
    description="Updates the password for an authenticated user session.",
    responses={
        200: {"description": "Password changed successfully", "model": APIResponse},
        404: {
            "description": "Result of change password data not found",
            "content": {"application/json": {"example": {"detail": "Result of change password data not found"}}},
        },
        **COMMON_500_RESPONSE,
    },
)
async def change_password(
    request: LogoutRequest,
    service: AuthService = Depends(),
):
    try:
        result = await service.change_password(request)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Result of change password data not found",
            )
        return {"status": "success", "code": 200, "data": result}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post(
    "/refresh_token",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Refresh JWT Token",
    description="Generates a new access token using a valid refresh token.",
    responses={
        200: {"description": "Token refreshed successfully", "model": APIResponse},
        401: {
            "description": "Invalid or expired refresh token",
            "content": {"application/json": {"example": {"detail": "Invalid or expired token"}}},
        },
    },
)
async def refresh_token_api(
    request: RefreshTokenRequest,
    service: AuthService = Depends(),
):
    try:
        response = await service.refresh_token(request.refresh_token)
        return {
            "status": "success",
            "code": 200,
            "data": response,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )

