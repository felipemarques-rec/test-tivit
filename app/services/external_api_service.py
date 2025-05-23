import httpx
import json
from typing import Dict, Any
from app.core.config import settings


class ExternalApiService:
    """Service to handle external API calls."""
    
    def __init__(self):
        self.base_url = settings.external_api_base_url
        self.timeout = 30.0
    
    async def get_health(self) -> Dict[str, Any]:
        """Get health status from external API."""
        return await self._make_request("GET", "health")
    
    async def get_user_data(self) -> Dict[str, Any]:
        """Get user data from external API."""
        return await self._make_request("GET", "user")
    
    async def get_admin_data(self) -> Dict[str, Any]:
        """Get admin data from external API."""
        return await self._make_request("GET", "admin")
    
    async def post_token_data(self, token_data: Dict[str, Any]) -> Dict[str, Any]:
        """Post token data to external API."""
        return await self._make_request("POST", "token", json_data=token_data)
    
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        json_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to external API."""
        url = f"{self.base_url}/{endpoint}"
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                if method.upper() == "GET":
                    response = await client.get(url)
                elif method.upper() == "POST":
                    response = await client.post(url, json=json_data)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                # Parse response data
                try:
                    if response.headers.get('content-type', '').startswith('application/json'):
                        data = response.json()
                    else:
                        data = {"text": response.text}
                except json.JSONDecodeError:
                    data = {"text": response.text}
                
                return {
                    "success": True,
                    "data": data,
                    "status_code": response.status_code,
                    "headers": dict(response.headers)
                }
                
        except httpx.TimeoutException:
            return {
                "success": False,
                "error": "Request timeout",
                "status_code": 408,
                "data": {}
            }
        except httpx.RequestError as e:
            return {
                "success": False,
                "error": f"Request error: {str(e)}",
                "status_code": 500,
                "data": {}
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "status_code": 500,
                "data": {}
            }


# Singleton instance
external_api_service = ExternalApiService()
