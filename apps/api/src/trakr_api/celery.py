"""Celery worker entrypoint.

Domain tasks are imported here so the worker registers them without making
the shared Celery app depend on those packages.
"""
from trakr_core.celery_app import celery_app
import discovery.tasks  # noqa: F401

__all__ = ["celery_app"]
