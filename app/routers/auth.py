from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.auth import Token, UserLogin, AuthResponse
from app.models.database import get_db
from app.domain.use_cases.authentication_use_case import AuthenticationUseCase
from app.domain.use_cases.external_api_use_case import ExternalApiUseCase
from app.infrastructure.repositories.fake_user_repository import FakeUserRepository
from app.infrastructure.repositories.sqlalchemy_external_data_repository import SqlAlchemyExternalDataRepository
from app.services.external_api_service import external_api_service

router = APIRouter(prefix="/auth", tags=["authentication"])


def get_auth_use_case() -> AuthenticationUseCase:
    """Get authentication use case instance."""
    user_repository = FakeUserRepository()
    return AuthenticationUseCase(user_repository)


def get_external_api_use_case(db: Session = Depends(get_db)) -> ExternalApiUseCase:
    """Get external API use case instance."""
    external_data_repository = SqlAlchemyExternalDataRepository(db)
    return ExternalApiUseCase(external_data_repository, external_api_service)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_use_case: AuthenticationUseCase = Depends(get_auth_use_case),
    external_api_use_case: ExternalApiUseCase = Depends(get_external_api_use_case)
):
    """Authenticate user and return JWT token using OAuth2 form data."""
    auth_result = auth_use_case.authenticate(form_data.username, form_data.password)
    
    if not auth_result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Send token data to external API
    token_data = {
        "username": auth_result["user"]["username"],
        "role": auth_result["user"]["role"],
        "token": auth_result["access_token"]
    }
    
    await external_api_use_case.send_token_data(token_data)
    
    return {
        "access_token": auth_result["access_token"],
        "token_type": auth_result["token_type"]
    }


@router.post("/token-json", response_model=Token)
async def login_with_json(
    user_login: UserLogin,
    auth_use_case: AuthenticationUseCase = Depends(get_auth_use_case),
    external_api_use_case: ExternalApiUseCase = Depends(get_external_api_use_case)
):
    """Authenticate user with JSON payload and return JWT token."""
    auth_result = auth_use_case.authenticate(user_login.username, user_login.password)
    
    if not auth_result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Send token data to external API
    token_data = {
        "username": auth_result["user"]["username"],
        "role": auth_result["user"]["role"],
        "token": auth_result["access_token"]
    }
    
    await external_api_use_case.send_token_data(token_data)
    
    return {
        "access_token": auth_result["access_token"],
        "token_type": auth_result["token_type"]
    }


@router.post("/login", response_model=AuthResponse)
async def login_detailed(
    user_login: UserLogin,
    auth_use_case: AuthenticationUseCase = Depends(get_auth_use_case),
    external_api_use_case: ExternalApiUseCase = Depends(get_external_api_use_case)
):
    """Authenticate user and return detailed response with user information."""
    auth_result = auth_use_case.authenticate(user_login.username, user_login.password)
    
    if not auth_result:
        return AuthResponse(
            success=False,
            message="Authentication failed. Invalid credentials.",
            data=None,
            user=None
        )
    
    # Send token data to external API
    token_data = {
        "username": auth_result["user"]["username"],
        "role": auth_result["user"]["role"],
        "token": auth_result["access_token"]
    }
    
    await external_api_use_case.send_token_data(token_data)
    
    return AuthResponse(
        success=True,
        message="Authentication successful",
        data=Token(
            access_token=auth_result["access_token"],
            token_type=auth_result["token_type"]
        ),
        user=auth_result["user"]
    )
