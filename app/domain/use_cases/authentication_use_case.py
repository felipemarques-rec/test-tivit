from typing import Optional, Dict, Any
from app.domain.entities.user import User, UserRole
from app.domain.repositories.user_repository import UserRepositoryInterface
from app.core.security import verify_password, create_access_token


class AuthenticationUseCase:
    """Use case for user authentication."""
    
    def __init__(self, user_repository: UserRepositoryInterface):
        self._user_repository = user_repository
    
    def authenticate(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user and return token data."""
        user = self._user_repository.get_by_username(username)
        
        if not user:
            return None
        
        if not user.is_active:
            return None
        
        if not user.password_hash or not verify_password(password, user.password_hash):
            return None
        
        # Create token with user data
        token_data = {
            "sub": user.username,
            "role": user.role.value
        }
        
        access_token = create_access_token(token_data)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "username": user.username,
                "role": user.role.value,
                "is_active": user.is_active
            }
        }
    
    def validate_user_access(self, user: User, required_role: UserRole) -> bool:
        """Validate if user has access to resources with required role."""
        if not user.is_active:
            return False
        
        if required_role == UserRole.ADMIN:
            return user.can_access_admin_resources()
        elif required_role == UserRole.USER:
            return user.can_access_user_resources()
        
        return False
