"""Main FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from trakr_api.api.jobs import router as jobs_router
from identity.api.auth import router as auth_router
from trakr_core.config import get_settings
from trakr_core.database import close_db, init_db
from documents.api import router as documents_router
from aircraft.api import router as aircraft_router
from aircraft_telemetry.api import router as aircraft_telemetry_router
from trakr_core.exceptions import (
    ServiceException,
    http_error_handler,
    request_validation_exception_handler,
)
from identity.api import router as users_router
from trakr_core.logging import get_logger, setup_logging
from trakr_core.schemas.errors import ErrorResponse

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(documents_router)
api_router.include_router(aircraft_router)
api_router.include_router(aircraft_telemetry_router)
api_router.include_router(jobs_router)

settings = get_settings()

setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def secure_headers(request: Request, call_next):
    try:
        response = await call_next(request)
        logger.info(f"{request.method} {request.url}")
    except Exception as exc:
        detail = str(exc) if settings.DEBUG else "An unexpected error occurred."
        logger.exception(detail)
        response = JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(
                error="Internal server error",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=detail,
            ).model_dump(exclude_unset=True, by_alias=True),
        )

    response.headers.setdefault(
        "Access-Control-Allow-Origin", request.headers.get("origin", "")
    )
    response.headers.setdefault("Access-Control-Allow-Credentials", "true")

    return response


@app.exception_handler(ServiceException)
async def service_exception_handler(
    request: Request, exc: ServiceException
) -> JSONResponse:
    """Handle service layer exceptions with standardized error format.

    Args:
        request: FastAPI request object
        exc: ServiceException instance

    Returns:
        JSONResponse with standardized error format
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail or "An error occurred",
            status_code=exc.status_code,
            detail=exc.detail,
        ).model_dump(exclude_unset=True, by_alias=True),
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return await http_error_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return await request_validation_exception_handler(request, exc)


# Include API router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Trakr API",
        "version": settings.VERSION,
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
