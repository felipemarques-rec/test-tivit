from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.external_data import ExternalApiData


class ExternalDataRepositoryInterface(ABC):
    """Abstract interface for external data repository."""
    
    @abstractmethod
    def save(self, data: ExternalApiData) -> ExternalApiData:
        """Save external API data."""
        pass
    
    @abstractmethod
    def get_by_id(self, data_id: int) -> Optional[ExternalApiData]:
        """Get external data by ID."""
        pass
    
    @abstractmethod
    def get_by_endpoint(self, endpoint: str, limit: int = 10) -> List[ExternalApiData]:
        """Get external data by endpoint."""
        pass
    
    @abstractmethod
    def get_all(self, limit: int = 100) -> List[ExternalApiData]:
        """Get all external data with limit."""
        pass
    
    @abstractmethod
    def delete_by_id(self, data_id: int) -> bool:
        """Delete external data by ID."""
        pass
