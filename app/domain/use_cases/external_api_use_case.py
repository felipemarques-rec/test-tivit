from typing import Dict, Any
from app.domain.entities.external_data import ExternalApiData
from app.domain.repositories.external_data_repository import ExternalDataRepositoryInterface
from app.services.external_api_service import ExternalApiService


class ExternalApiUseCase:
    """Use case for external API operations."""
    
    def __init__(
        self, 
        external_data_repository: ExternalDataRepositoryInterface,
        external_api_service: ExternalApiService
    ):
        self._external_data_repository = external_data_repository
        self._external_api_service = external_api_service
    
    async def fetch_and_store_health_data(self) -> Dict[str, Any]:
        """Fetch health data from external API and store it."""
        try:
            response = await self._external_api_service.get_health()
            
            external_data = ExternalApiData(
                endpoint="health",
                data=response.get("data", {}),
                status_code=response.get("status_code", 500)
            )
            
            saved_data = self._external_data_repository.save(external_data)
            
            return {
                "success": True,
                "data": saved_data.data,
                "stored_id": saved_data.id,
                "status_code": saved_data.status_code
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "status_code": 500
            }
    
    async def fetch_and_store_user_data(self) -> Dict[str, Any]:
        """Fetch user data from external API and store it."""
        try:
            response = await self._external_api_service.get_user_data()
            
            external_data = ExternalApiData(
                endpoint="user",
                data=response.get("data", {}),
                status_code=response.get("status_code", 500)
            )
            
            saved_data = self._external_data_repository.save(external_data)
            
            return {
                "success": True,
                "data": saved_data.data,
                "stored_id": saved_data.id,
                "status_code": saved_data.status_code
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "status_code": 500
            }
    
    async def fetch_and_store_admin_data(self) -> Dict[str, Any]:
        """Fetch admin data from external API and store it."""
        try:
            response = await self._external_api_service.get_admin_data()
            
            external_data = ExternalApiData(
                endpoint="admin",
                data=response.get("data", {}),
                status_code=response.get("status_code", 500)
            )
            
            saved_data = self._external_data_repository.save(external_data)
            
            return {
                "success": True,
                "data": saved_data.data,
                "stored_id": saved_data.id,
                "status_code": saved_data.status_code
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "status_code": 500
            }
    
    async def send_token_data(self, token_data: Dict[str, Any]) -> Dict[str, Any]:
        """Send token data to external API and store response."""
        try:
            response = await self._external_api_service.post_token_data(token_data)
            
            external_data = ExternalApiData(
                endpoint="token",
                data={
                    "request": token_data,
                    "response": response.get("data", {})
                },
                status_code=response.get("status_code", 500)
            )
            
            saved_data = self._external_data_repository.save(external_data)
            
            return {
                "success": True,
                "data": saved_data.data,
                "stored_id": saved_data.id,
                "status_code": saved_data.status_code
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "status_code": 500
            }
