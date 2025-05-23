from dataclasses import dataclass
from typing import Optional
from enum import Enum


class UserRole(Enum):
    USER = "user"
    ADMIN = "admin"


@dataclass
class User:
    """User domain entity."""
    username: str
    role: UserRole
    is_active: bool = True
    password_hash: Optional[str] = None
    
    def has_role(self, required_role: UserRole) -> bool:
        """Check if user has the required role."""
        return self.role == required_role
    
    def is_admin(self) -> bool:
        """Check if user is admin."""
        return self.role == UserRole.ADMIN
    
    def is_user(self) -> bool:
        """Check if user is regular user."""
        return self.role == UserRole.USER
    
    def can_access_admin_resources(self) -> bool:
        """Check if user can access admin resources."""
        return self.is_active and self.is_admin()
    
    def can_access_user_resources(self) -> bool:
        """Check if user can access user resources."""
        return self.is_active and (self.is_user() or self.is_admin())
