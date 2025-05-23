from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional


@dataclass
class ExternalApiData:
    """External API data domain entity."""
    endpoint: str
    data: Dict[str, Any]
    status_code: int
    created_at: Optional[datetime] = None
    id: Optional[int] = None
    
    def is_successful(self) -> bool:
        """Check if the API call was successful."""
        return 200 <= self.status_code < 300
    
    def is_client_error(self) -> bool:
        """Check if there was a client error."""
        return 400 <= self.status_code < 500
    
    def is_server_error(self) -> bool:
        """Check if there was a server error."""
        return self.status_code >= 500
    
    def get_error_type(self) -> str:
        """Get the type of error if any."""
        if self.is_successful():
            return "none"
        elif self.is_client_error():
            return "client_error"
        elif self.is_server_error():
            return "server_error"
        else:
            return "unknown"
