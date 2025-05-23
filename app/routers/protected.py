from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.auth import require_user_role, require_admin_role
from app.models.database import get_db
from app.schemas.external_data import ApiResponse
from app.domain.entities.user import User
from app.domain.use_cases.external_api_use_case import ExternalApiUseCase
from app.infrastructure.repositories.sqlalchemy_external_data_repository import SqlAlchemyExternalDataRepository
from app.services.external_api_service import external_api_service

router = APIRouter(tags=["protected"])


def get_external_api_use_case(db: Session = Depends(get_db)) -> ExternalApiUseCase:
    """Get external API use case instance."""
    external_data_repository = SqlAlchemyExternalDataRepository(db)
    return ExternalApiUseCase(external_data_repository, external_api_service)


@router.get("/user", response_model=ApiResponse)
async def get_user_endpoint(
    current_user: User = Depends(require_user_role),
    external_api_use_case: ExternalApiUseCase = Depends(get_external_api_use_case)
):
    """Protected endpoint accessible only by users with 'user' role."""
    # Fetch data from external API and store in database
    result = await external_api_use_case.fetch_and_store_user_data()
    
    if result["success"]:
        return ApiResponse(
            success=True,
            message="User data retrieved successfully",
            data={
                "user_info": {
                    "username": current_user.username,
                    "role": current_user.role.value,
                    "is_active": current_user.is_active
                },
                "external_data": result["data"],
                "stored_id": result.get("stored_id")
            },
            status_code=result.get("status_code"),
            stored_id=result.get("stored_id")
        )
    else:
        return ApiResponse(
            success=False,
            message=f"Failed to retrieve user data: {result.get('error', 'Unknown error')}",
            data=None,
            error=result.get("error"),
            status_code=result.get("status_code", 500)
        )


@router.get("/admin", response_model=ApiResponse)
async def get_admin_endpoint(
    current_user: User = Depends(require_admin_role),
    external_api_use_case: ExternalApiUseCase = Depends(get_external_api_use_case)
):
    """Protected endpoint accessible only by users with 'admin' role."""
    # Fetch data from external API and store in database
    result = await external_api_use_case.fetch_and_store_admin_data()
    
    if result["success"]:
        return ApiResponse(
            success=True,
            message="Admin data retrieved successfully",
            data={
                "admin_info": {
                    "username": current_user.username,
                    "role": current_user.role.value,
                    "is_active": current_user.is_active
                },
                "external_data": result["data"],
                "stored_id": result.get("stored_id")
            },
            status_code=result.get("status_code"),
            stored_id=result.get("stored_id")
        )
    else:
        return ApiResponse(
            success=False,
            message=f"Failed to retrieve admin data: {result.get('error', 'Unknown error')}",
            data=None,
            error=result.get("error"),
            status_code=result.get("status_code", 500)
        )


@router.get("/external-health", response_model=ApiResponse)
async def get_external_health_endpoint(
    current_user: User = Depends(require_user_role),
    external_api_use_case: ExternalApiUseCase = Depends(get_external_api_use_case)
):
    """External health check endpoint accessible by authenticated users."""
    # Fetch health data from external API and store in database
    result = await external_api_use_case.fetch_and_store_health_data()
    
    if result["success"]:
        return ApiResponse(
            success=True,
            message="External health check completed successfully",
            data={
                "health_status": result["data"],
                "stored_id": result.get("stored_id"),
                "checked_by": {
                    "username": current_user.username,
                    "role": current_user.role.value
                }
            },
            status_code=result.get("status_code"),
            stored_id=result.get("stored_id")
        )
    else:
        return ApiResponse(
            success=False,
            message=f"External health check failed: {result.get('error', 'Unknown error')}",
            data=None,
            error=result.get("error"),
            status_code=result.get("status_code", 500)
        )


@router.get("/profile", response_model=ApiResponse)
async def get_user_profile(
    current_user: User = Depends(require_user_role)
):
    """Get current user profile information."""
    return ApiResponse(
        success=True,
        message="User profile retrieved successfully",
        data={
            "username": current_user.username,
            "role": current_user.role.value,
            "is_active": current_user.is_active,
            "permissions": {
                "can_access_user_resources": current_user.can_access_user_resources(),
                "can_access_admin_resources": current_user.can_access_admin_resources(),
                "is_admin": current_user.is_admin(),
                "is_user": current_user.is_user()
            }
        },
        status_code=200
    )
