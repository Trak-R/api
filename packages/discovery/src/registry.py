"""Provider service registry: returns provider services (each holds its client)."""

from __future__ import annotations

from typing import Any, Protocol

from trakr_core.clients.serper import SerperClient
from discovery.schemas.discovery import ProviderDiscoveryRequest, ProviderDiscoveryResult
from discovery.services.serper import SerperService


class ProviderServiceProtocol(Protocol):
    async def search(self, request: ProviderDiscoveryRequest) -> ProviderDiscoveryResult: ...


def default_provider_services() -> dict[str, ProviderServiceProtocol]:
    return {
        SerperClient.provider: SerperService(client=SerperClient()),
    }

