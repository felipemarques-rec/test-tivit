from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.user import User


class UserRepositoryInterface(ABC):
    """Abstract interface for user repository."""
    
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        pass
    
    @abstractmethod
    def create(self, user: User) -> User:
        """Create a new user."""
        pass
    
    @abstractmethod
    def update(self, user: User) -> User:
        """Update an existing user."""
        pass
    
    @abstractmethod
    def delete(self, username: str) -> bool:
        """Delete a user by username."""
        pass
    
    @abstractmethod
    def exists(self, username: str) -> bool:
        """Check if user exists."""
        pass
