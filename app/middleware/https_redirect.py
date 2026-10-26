"""Redirección a HTTPS cuando el despliegue exige TLS (EN-003 / RNF-003)."""

from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

from app.core.config import get_settings


class HttpsRedirectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        settings = get_settings()
        if not settings.force_https:
            return await call_next(request)
        if request.url.scheme == "https":
            return await call_next(request)
        forwarded = request.headers.get("x-forwarded-proto", "").split(",")[0].strip().lower()
        if forwarded == "https":
            return await call_next(request)
        target = request.url.replace(scheme="https")
        return RedirectResponse(str(target), status_code=308)
