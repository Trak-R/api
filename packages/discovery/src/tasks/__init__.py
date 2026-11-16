"""Discovery Celery tasks."""
from discovery.tasks.jobs.discovery import crawl_page, crawl_page_hit  # noqa: F401
from discovery.tasks.orchestrators.discovery import orchestrate_discovery  # noqa: F401

__all__ = ["crawl_page", "crawl_page_hit", "orchestrate_discovery"]
