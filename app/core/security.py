from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.core.config import settings
import secrets
import hashlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Fake users database with hashed passwords and secure role validation
fake_users_db = {
    "usuario": {
        "username": "usuario",
        "role": "user",
        "password_hash": pwd_context.hash("L0XuwPOdS5U"),
        "is_active": True,
        "role_hash": hashlib.sha256("user".encode()).hexdigest()
    },
    "admin": {
        "username": "admin",
        "role": "admin", 
        "password_hash": pwd_context.hash("JKSipm0YH"),
        "is_active": True,
        "role_hash": hashlib.sha256("admin".encode()).hexdigest()
    }
}

# Valid roles with their hashes for security
VALID_ROLES = {
    "user": hashlib.sha256("user".encode()).hexdigest(),
    "admin": hashlib.sha256("admin".encode()).hexdigest()
}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate password hash."""
    return pwd_context.hash(password)


def validate_role(role: str, role_hash: str) -> bool:
    """Validate role integrity using hash comparison."""
    expected_hash = VALID_ROLES.get(role)
    return expected_hash is not None and secrets.compare_digest(expected_hash, role_hash)


def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticate user with username and password with enhanced security."""
    # Prevent timing attacks by always performing hash operation
    dummy_hash = "$2b$12$dummy.hash.to.prevent.timing.attacks"
    
    user = fake_users_db.get(username)
    if not user:
        # Perform dummy verification to prevent timing attacks
        pwd_context.verify(password, dummy_hash)
        return None
    
    if not user.get("is_active", False):
        return None
        
    if not verify_password(password, user["password_hash"]):
        return None
    
    # Validate role integrity
    if not validate_role(user["role"], user["role_hash"]):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Security violation detected"
        )
    
    return {
        "username": user["username"],
        "role": user["role"],
        "is_active": user["is_active"]
    }


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token with enhanced security."""
    to_encode = data.copy()
    
    # Add security claims
    now = datetime.utcnow()
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.access_token_expire_minutes)
    
    # Add standard JWT claims
    to_encode.update({
        "exp": expire,
        "iat": now,
        "nbf": now,
        "jti": secrets.token_urlsafe(32),  # JWT ID for token revocation
        "iss": "teste-tivit-api",  # Issuer
        "aud": "teste-tivit-client"  # Audience
    })
    
    # Add role hash for integrity verification
    if "role" in to_encode:
        to_encode["role_hash"] = hashlib.sha256(to_encode["role"].encode()).hexdigest()
    
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str) -> Dict[str, Any]:
    """Verify and decode JWT token with enhanced security validation."""
    try:
        payload = jwt.decode(
            token, 
            settings.secret_key, 
            algorithms=[settings.algorithm],
            audience="teste-tivit-client",
            issuer="teste-tivit-api"
        )
        
        username: str = payload.get("sub")
        role: str = payload.get("role")
        role_hash: str = payload.get("role_hash")
        
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing subject",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not role or not role_hash:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing role information",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Validate role integrity
        if not validate_role(role, role_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: role tampering detected",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verify user still exists and is active
        user = fake_users_db.get(username)
        if not user or not user.get("is_active", False):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return payload
        
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_user_from_token(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Extract user information from validated token payload."""
    username = payload.get("sub")
    user = fake_users_db.get(username)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {
        "username": user["username"],
        "role": user["role"],
        "is_active": user["is_active"]
    }
