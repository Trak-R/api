"""Discovery API routes.

Triggers a Celery orchestrator that enqueues per-URL crawl jobs.
"""

from typing import List
from fastapi import APIRouter, Depends, status

from identity.dependencies import authorization
from trakr_core.exceptions import ERROR_RESPONSES
from identity.models.user import User
from discovery.schemas.discovery import DiscoveryJobResponse, DiscoveryRequest, ProviderDiscoveryRequest, ProductRecord
from discovery.services.discovery import DiscoveryService, ProviderDiscoveryResponse
from discovery.tasks.orchestrators.discovery import orchestrate_discovery

router = APIRouter(prefix="/discovery", tags=["Discovery"])


@router.post(
    "",
    status_code=status.HTTP_202_ACCEPTED,
    responses=ERROR_RESPONSES,
    summary="Trigger discovery crawl for a list of URLs from CommonCrawl. Loads the application-tagged results into S3.",
)
async def start_discovery(
    request: DiscoveryRequest,
    # current_user: User = Depends(authorization()),
) -> DiscoveryJobResponse:
    result = orchestrate_discovery.delay(
        urls=request.urls,
        data_origin=request.data_origin,
        target_application=request.target_application,
        crawl=request.crawl,
        user_id=None,
        seed_url=request.seed_url,
        match_type=request.match_type,
        max_urls=request.max_urls,
        page_size=request.page_size,
        url_regex=request.url_regex,
    )
    return DiscoveryJobResponse(job_id=result.id)

@router.post(
    "/offers/search",
    status_code=status.HTTP_200_OK,
    summary="Search offers via external providers and return normalized results.",
)
async def offer_discovery(
    requests: List[ProviderDiscoveryRequest],
) -> ProviderDiscoveryResponse[ProductRecord]:
    _service = DiscoveryService()
    return await _service.discover_offers(requests)


@router.post(
    "/offers/enrichment",
    status_code=status.HTTP_200_OK,
    summary="Retrieve specific normalized details from providers.",
)
async def search(
    requests: List[ProviderDiscoveryRequest],
) -> ProviderDiscoveryResponse[ProductRecord]:
    _service = DiscoveryService()
    return await _service.discover_offers(requests)
