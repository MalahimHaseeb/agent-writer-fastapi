"""FastAPI application entry point."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import sys

from config import get_settings
from logger import setup_logger
from responses import APIResponse, StatusCode
from api import router as api_router

logger = setup_logger(__name__)

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered blog writing agent using Gemini and Tavily",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"[Exception] {type(exc).__name__}: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content=APIResponse.error(
            message="Internal server error",
            error=str(exc),
            status=StatusCode.INTERNAL_ERROR
        ).model_dump()
    )


@app.middleware("http")
async def add_request_logging(request: Request, call_next):
    logger.info(f"[Request] {request.method} {request.url.path}")

    response = await call_next(request)

    logger.info(f"[Response] {request.method} {request.url.path} - {response.status_code}")
    return response


@app.on_event("startup")
async def startup_event():
    logger.info("=" * 50)
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.API_ENV}")
    logger.info(f"Debug: {settings.DEBUG}")
    logger.info(f"Server: http://{settings.API_HOST}:{settings.API_PORT}")
    logger.info("=" * 50)

    try:
        settings.validate_api_keys()
        logger.info("✅ API keys configured successfully")
    except ValueError as e:
        logger.error(f"❌ Configuration error: {str(e)}")
        sys.exit(1)


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down application...")


app.include_router(api_router)


@app.get("/", response_model=APIResponse[dict])
async def root():
    return APIResponse.success(
        data={
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "endpoints": {
                "docs": "/docs",
                "redoc": "/redoc",
                "openapi": "/openapi.json",
                "health": "/api/health",
                "generate_blog": "/api/generate-blog",
                "sessions": "/api/sessions",
                "create_session": "/api/session",
            }
        },
        message="Welcome to Blog Writing Agent API"
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level="info",
    )
