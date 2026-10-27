"""Aplicación FastAPI de EcoLogística Huancayo."""

import logging

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app import __version__
from app.api.v1.auth import router as auth_router
from app.api.v1.desk import router as desk_router
from app.api.v1.plate_restrictions import router as plate_restrictions_router
from app.api.v1.routes import API_DESCRIPTION, OPENAPI_TAGS, register_exception_handlers, router
from app.api.v1.websockets import router as ws_router
from app.core.config import get_settings
from app.core.database import get_db
from app.core.security_boot import validate_security_settings
from app.middleware.https_redirect import HttpsRedirectMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware

logger = logging.getLogger("ecologistica.boot")


@asynccontextmanager
async def lifespan(_: FastAPI):
    settings = get_settings()
    validate_security_settings(settings)
    logger.info("Entorno %s — controles de seguridad verificados.", settings.app_environment)
    yield


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=__version__,
    summary="Optimización ecológica de última milla en Huancayo.",
    description=API_DESCRIPTION,
    openapi_tags=OPENAPI_TAGS,
    swagger_ui_parameters={"docExpansion": "list", "displayRequestDuration": True},
    docs_url="/docs" if settings.expose_api_docs else None,
    redoc_url="/redoc" if settings.expose_api_docs else None,
    openapi_url="/openapi.json" if settings.expose_api_docs else None,
    lifespan=lifespan,
)
app.add_middleware(HttpsRedirectMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins(),
    allow_methods=["GET", "POST", "PATCH", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)
register_exception_handlers(app)
app.include_router(router)
app.include_router(auth_router)
app.include_router(desk_router)
app.include_router(plate_restrictions_router)
app.include_router(ws_router)


def custom_openapi() -> dict:
    """Esquema OpenAPI con la convención del Quinual visible para el mapa."""
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title=app.title,
        version=app.version,
        summary=app.summary,
        description=app.description,
        routes=app.routes,
        tags=OPENAPI_TAGS,
    )
    schema["info"]["x-huancayo"] = {
        "centro": [settings.huancayo_base_lon, settings.huancayo_base_lat],
        "quinual_kg_co2_por_ano": settings.quinual_kg_co2_per_year,
    }
    app.openapi_schema = schema
    return schema


app.openapi = custom_openapi


@app.get("/health", tags=["sistema"])
async def health() -> dict[str, str]:
    """Comprueba que el proceso está en pie, sin tocar la base de datos."""
    return {"status": "ok", "service": settings.app_name}


@app.get("/health/db", tags=["sistema"])
async def health_db(session: AsyncSession = Depends(get_db)) -> dict[str, str]:
    """Comprueba PostgreSQL y devuelve la versión de PostGIS."""
    postgis_version = await session.scalar(text("SELECT PostGIS_Version()"))
    return {"status": "ok", "postgis": str(postgis_version)}
