"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.routes import upload, extraction, verification, analytics

# Initialize settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title="Policy AI Lens API",
    description="AI-powered insurance policy data extraction system",
    version="0.1.0",
    debug=settings.debug
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/api/v1", tags=["upload"])
app.include_router(extraction.router, prefix="/api/v1", tags=["extraction"])
app.include_router(
    verification.router,
    prefix="/api/v1",
    tags=["verification"])
app.include_router(analytics.router, prefix="/api/v1", tags=["analytics"])


@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {
        "message": "Policy AI Lens API",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
