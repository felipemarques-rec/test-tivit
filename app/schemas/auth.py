from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from enum import Enum


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class Token(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")


class TokenData(BaseModel):
    username: Optional[str] = Field(None, description="Username from token")
    role: Optional[UserRole] = Field(None, description="User role from token")


class UserLogin(BaseModel):
    username: str = Field(..., min_length=1, max_length=50, description="Username")
    password: str = Field(..., min_length=1, max_length=100, description="Password")
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        if not v.strip():
            raise ValueError('Username cannot be empty or whitespace')
        return v.strip()
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if not v:
            raise ValueError('Password cannot be empty')
        return v


class User(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    
    username: str = Field(..., description="Username")
    role: UserRole = Field(..., description="User role")
    is_active: bool = Field(default=True, description="User active status")


class UserInDB(User):
    password_hash: Optional[str] = Field(None, description="Hashed password")


class AuthResponse(BaseModel):
    success: bool = Field(..., description="Authentication success status")
    message: str = Field(..., description="Response message")
    data: Optional[Token] = Field(None, description="Token data if successful")
    user: Optional[User] = Field(None, description="User information if successful")
