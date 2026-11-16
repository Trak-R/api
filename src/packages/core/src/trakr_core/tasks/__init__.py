"""Shared Celery tasks."""

from trakr_core.celery_app import celery_app
from trakr_core.tasks.example import hello_world, process_data  # noqa: F401

__all__ = ["celery_app", "hello_world", "process_data"]
