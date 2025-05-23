from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any
from app.core.security import verify_token, get_user_from_token
from app.domain.entities.user import User, UserRole
from app.infrastructure.repositories.fake_user_repository import FakeUserRepository

security = HTTPBearer()

# Singleton instances
_user_repository = FakeUserRepository()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current authenticated user from JWT token."""
    token = credentials.credentials
    payload = verify_token(token)
    
    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing username",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = _user_repository.get_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def get_current_user_role(current_user: User = Depends(get_current_user)) -> UserRole:
    """Get current user role."""
    return current_user.role


async def require_user_role(current_user: User = Depends(get_current_user)) -> User:
    """Require user role for access."""
    if not current_user.can_access_user_resources():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. User role required and account must be active."
        )
    return current_user


async def require_admin_role(current_user: User = Depends(get_current_user)) -> User:
    """Require admin role for access."""
    if not current_user.can_access_admin_resources():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin role required and account must be active."
        )
    return current_user


async def require_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Require active user account."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Account is inactive."
        )
    return current_user


def get_user_repository() -> FakeUserRepository:
    """Get user repository instance."""
    return _user_repository
