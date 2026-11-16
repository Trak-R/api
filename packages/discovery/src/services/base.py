"""Base class for provider discovery services."""
from __future__ import annotations

from abc import ABC
from collections.abc import Awaitable, Callable
from typing import Any

import httpx

from discovery.schemas.discovery import ProviderDiscoveryError, ProviderDiscoveryResult


class BaseDiscoveryService(ABC):
    """Base for provider discovery services. Owns error handling; subclasses implement success normalization."""

    def __init__(self, *, client: Any) -> None:
        """Initialize with a provider client (context manager with .provider and .fetch(request))."""
        self._client = client

    @staticmethod
    def _safe_text(resp: httpx.Response) -> str:
        """Return response body text for error details, capped at 2000 chars."""
        try:
            txt = resp.text or ""
        except Exception:
            return ""
        return txt[:2000]

    def _is_missing_api_key(self) -> bool:
        """Return True if the client has no API key. Subclasses may override."""
        return not getattr(self._client, "_api_key", None)

    def _error_result(
        self,
        code: str,
        message: str,
        details: str | None = None,
    ) -> ProviderDiscoveryResult:
        """Build a failed ProviderDiscoveryResult."""
        return ProviderDiscoveryResult(
            provider=self._client.provider,
            results=[],
            error=ProviderDiscoveryError(code=code, message=message, details=details),
        )

    async def _execute_fetch(
        self,
        coro: Callable[[], Awaitable[httpx.Response]],
        normalizer: Callable[[httpx.Response], Awaitable[ProviderDiscoveryResult]],
    ) -> ProviderDiscoveryResult:
        """Run fetch coroutine; on 2xx call normalizer(resp), on error return ProviderDiscoveryResult."""
        async with self._client:
            try:
                resp = await coro()
            except ValueError as e:
                if "API key" in str(e):
                    return self._error_result("missing_api_key", str(e))
                raise
            except httpx.TimeoutException as e:
                return self._error_result("timeout", "Request timed out", str(e))
            except httpx.HTTPError as e:
                return self._error_result("http_error", "HTTP request failed", str(e))

            if 200 <= resp.status_code < 300:
                return await normalizer(resp)

            if resp.status_code in (401, 403):
                return self._error_result(
                    "auth_error",
                    "Authentication failed.",
                    self._safe_text(resp),
                )
            if resp.status_code == 429:
                return self._error_result(
                    "rate_limited",
                    "Rate limit exceeded.",
                    self._safe_text(resp),
                )
            if 500 <= resp.status_code < 600:
                return self._error_result(
                    "provider_error",
                    f"Request failed (status={resp.status_code}).",
                    self._safe_text(resp),
                )
            return self._error_result(
                "provider_error",
                f"Request failed (status={resp.status_code}).",
                self._safe_text(resp),
            )
