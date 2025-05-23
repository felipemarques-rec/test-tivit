from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from app.routers import auth, protected
from app.models.database import engine, Base
from app.core.config import settings
from app.schemas.external_data import HealthCheckResponse, ErrorResponse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.error(f"Failed to create database tables: {e}")

app = FastAPI(
    title="Teste Tivit API",
    description="""
    API desenvolvida para o teste técnico da Tivit com:
    
    - **Autenticação JWT** com segurança aprimorada
    - **Controle de Acesso** baseado em roles (user/admin)
    - **Integração Externa** com armazenamento em banco de dados
    - **Arquitetura Limpa** seguindo princípios SOLID
    - **Validações Robustas** de entrada de dados
    - **Proteção contra Ataques** de timing e role tampering
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "Teste Tivit API",
        "email": "contato@exemplo.com",
    },
    license_info={
        "name": "MIT",
    },
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


# Global exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            status_code=exc.status_code
        ).model_dump()
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request, exc):
    """Handle SQLAlchemy database errors."""
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Database error occurred",
            detail="Please try again later",
            status_code=500
        ).model_dump()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail="An unexpected error occurred",
            status_code=500
        ).model_dump()
    )


# Include routers
app.include_router(auth.router)
app.include_router(protected.router)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Teste Tivit API",
        "version": "1.0.0",
        "description": "API com autenticação JWT segura e integração com serviços externos",
        "features": [
            "JWT Authentication with enhanced security",
            "Role-based access control (user/admin)",
            "External API integration with data storage",
            "Clean Architecture implementation",
            "SOLID principles compliance",
            "Comprehensive input validation",
            "Protection against timing attacks and role tampering"
        ],
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health",
            "auth": "/auth",
            "protected": ["/user", "/admin", "/profile"]
        }
    }


@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint."""
    try:
        # Test database connection
        from app.models.database import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        database_connected = True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        database_connected = False
    
    return HealthCheckResponse(
        status="healthy" if database_connected else "unhealthy",
        database_connected=database_connected
    )


@app.get("/info")
async def api_info():
    """Get detailed API information."""
    return {
        "api": {
            "name": "Teste Tivit API",
            "version": "1.0.0",
            "description": "Secure JWT API with Clean Architecture"
        },
        "security": {
            "authentication": "JWT Bearer Token",
            "roles": ["user", "admin"],
            "features": [
                "Password hashing with bcrypt",
                "Role integrity validation",
                "Token tampering protection",
                "Timing attack prevention",
                "Secure token claims (iss, aud, jti, etc.)"
            ]
        },
        "architecture": {
            "pattern": "Clean Architecture",
            "principles": ["SOLID", "Dependency Inversion", "Separation of Concerns"],
            "layers": [
                "Domain (Entities, Use Cases, Repositories)",
                "Infrastructure (Database, External APIs)",
                "Application (Controllers, Dependencies)",
                "Presentation (Routers, Schemas)"
            ]
        },
        "external_integrations": [
            "https://api-onecloud.multicloud.tivit.com/fake/health",
            "https://api-onecloud.multicloud.tivit.com/fake/user",
            "https://api-onecloud.multicloud.tivit.com/fake/admin",
            "https://api-onecloud.multicloud.tivit.com/fake/token"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info",
        access_log=True
    )
