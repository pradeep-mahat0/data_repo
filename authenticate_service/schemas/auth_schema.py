from enum import Enum
from typing import Any, Optional, List
from pydantic import BaseModel, EmailStr, Field


class AuthRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    MANAGER = "manager"
    COACH = "coach"


class AuthRequest(BaseModel):
    email: str = Field(..., description="User corporate or primary email address", example="user@company.com")
    password: str = Field(..., description="User password", example="SecurePass123!")
    program_name: Optional[str] = Field(None, description="Optional program name context")


class AuthenticateResponse(BaseModel):
    id: str = Field(..., description="User ID")
    fullName: str = Field(..., description="Full Name of the user")
    email: str = Field(..., description="Email address")
    role: str = Field(..., description="User role")
    token: str = Field(..., description="JWT Access Token")
    refresh_token: str = Field(..., description="JWT Refresh Token")
    status: str = Field(default="active", description="Account status")
    profile_pic: Optional[str] = Field(None, description="Profile picture URL")
    program_name: Optional[str] = Field(None, description="Current program name")


class AuthorizeResponse(BaseModel):
    id: str = Field(..., description="User unique identifier")
    fullName: str = Field(..., description="Full Name")
    email: str = Field(..., description="User Email")
    role: AuthRole = Field(..., description="Role assigned to user")
    managerId: Optional[str] = Field("", description="Manager's ID")
    managerName: Optional[str] = Field("", description="Manager's Full Name")
    status: str = Field(default="active", description="Account status")
    profile_pic: Optional[str] = Field("", description="Profile image URL")
    token: str = Field(..., description="Access token")
    refresh_token: str = Field(..., description="Refresh token")
    createdby: Optional[str] = Field("", description="Created by user ID")
    updatedby: Optional[str] = Field("", description="Updated by user ID")
    createdat: Optional[str] = Field("", description="Creation timestamp")
    updatedat: Optional[str] = Field("", description="Last update timestamp")
    external_email: Optional[str] = Field("", description="External email address")
    program_name: Optional[str] = Field("", description="Program name")


class listPrograms(BaseModel):
    program_name: str = Field(..., description="Unique program identifier")
    display_name: str = Field(..., description="Display label for program")


class AuthResponse(BaseModel):
    message: str = Field(..., description="Status message")
    user: Optional[AuthorizeResponse] = None


class APIResponse(BaseModel):
    status: str = Field("success", description="Status string: success or error")
    code: int = Field(200, description="HTTP status code")
    data: Optional[Any] = Field(None, description="Response payload")


class LogoutRequest(BaseModel):
    id: Optional[str] = Field(None, description="User ID or identifier")
    email: Optional[str] = Field(None, description="User email for logout/password operations")
    token: Optional[str] = Field(None, description="Token to invalidate")
    new_password: Optional[str] = Field(None, description="Used in reset/change password")
    old_password: Optional[str] = Field(None, description="Used in change password")
    reset_token: Optional[str] = Field(None, description="Token used in reset password")


class LogoutResponse(BaseModel):
    message: str = Field(..., description="Status message detailing operation outcome")


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., description="Valid JWT refresh token", example="eyJhbGciOiJIUzI1NiIsIn...")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600


class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Human-readable error details")

