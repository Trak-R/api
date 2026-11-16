"""Celery worker entrypoint.

Re-exports the shared Celery app so workers start with `trakr_api.celery`.
Import domain task modules here when a domain registers tasks.
"""
from trakr_core.celery_app import celery_app

__all__ = ["celery_app"]
