from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.entities.external_data import ExternalApiData
from app.domain.repositories.external_data_repository import ExternalDataRepositoryInterface
from app.models.external_data import ExternalData
import json


class SqlAlchemyExternalDataRepository(ExternalDataRepositoryInterface):
    """SQLAlchemy implementation of external data repository."""
    
    def __init__(self, db_session: Session):
        self._db_session = db_session
    
    def save(self, data: ExternalApiData) -> ExternalApiData:
        """Save external API data."""
        db_data = ExternalData(
            endpoint=data.endpoint,
            data=json.dumps(data.data),
            status_code=data.status_code
        )
        
        self._db_session.add(db_data)
        self._db_session.commit()
        self._db_session.refresh(db_data)
        
        return ExternalApiData(
            id=db_data.id,
            endpoint=db_data.endpoint,
            data=json.loads(db_data.data),
            status_code=db_data.status_code,
            created_at=db_data.created_at
        )
    
    def get_by_id(self, data_id: int) -> Optional[ExternalApiData]:
        """Get external data by ID."""
        db_data = self._db_session.query(ExternalData).filter(
            ExternalData.id == data_id
        ).first()
        
        if not db_data:
            return None
        
        return ExternalApiData(
            id=db_data.id,
            endpoint=db_data.endpoint,
            data=json.loads(db_data.data),
            status_code=db_data.status_code,
            created_at=db_data.created_at
        )
    
    def get_by_endpoint(self, endpoint: str, limit: int = 10) -> List[ExternalApiData]:
        """Get external data by endpoint."""
        db_data_list = self._db_session.query(ExternalData).filter(
            ExternalData.endpoint == endpoint
        ).order_by(ExternalData.created_at.desc()).limit(limit).all()
        
        return [
            ExternalApiData(
                id=db_data.id,
                endpoint=db_data.endpoint,
                data=json.loads(db_data.data),
                status_code=db_data.status_code,
                created_at=db_data.created_at
            )
            for db_data in db_data_list
        ]
    
    def get_all(self, limit: int = 100) -> List[ExternalApiData]:
        """Get all external data with limit."""
        db_data_list = self._db_session.query(ExternalData).order_by(
            ExternalData.created_at.desc()
        ).limit(limit).all()
        
        return [
            ExternalApiData(
                id=db_data.id,
                endpoint=db_data.endpoint,
                data=json.loads(db_data.data),
                status_code=db_data.status_code,
                created_at=db_data.created_at
            )
            for db_data in db_data_list
        ]
    
    def delete_by_id(self, data_id: int) -> bool:
        """Delete external data by ID."""
        db_data = self._db_session.query(ExternalData).filter(
            ExternalData.id == data_id
        ).first()
        
        if not db_data:
            return False
        
        self._db_session.delete(db_data)
        self._db_session.commit()
        return True
