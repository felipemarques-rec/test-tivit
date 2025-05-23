from typing import Optional
from app.domain.entities.user import User, UserRole
from app.domain.repositories.user_repository import UserRepositoryInterface
from app.core.security import get_password_hash


class FakeUserRepository(UserRepositoryInterface):
    """In-memory implementation of user repository for testing purposes."""
    
    def __init__(self):
        # Initialize with fake users as specified in requirements
        self._users = {
            "usuario": User(
                username="usuario",
                role=UserRole.USER,
                is_active=True,
                password_hash=get_password_hash("L0XuwPOdS5U")
            ),
            "admin": User(
                username="admin",
                role=UserRole.ADMIN,
                is_active=True,
                password_hash=get_password_hash("JKSipm0YH")
            )
        }
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self._users.get(username)
    
    def create(self, user: User) -> User:
        """Create a new user."""
        if self.exists(user.username):
            raise ValueError(f"User {user.username} already exists")
        
        self._users[user.username] = user
        return user
    
    def update(self, user: User) -> User:
        """Update an existing user."""
        if not self.exists(user.username):
            raise ValueError(f"User {user.username} does not exist")
        
        self._users[user.username] = user
        return user
    
    def delete(self, username: str) -> bool:
        """Delete a user by username."""
        if username in self._users:
            del self._users[username]
            return True
        return False
    
    def exists(self, username: str) -> bool:
        """Check if user exists."""
        return username in self._users
