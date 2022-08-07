"""Describe project apps."""
from django.apps import AppConfig


class BboardConfig(AppConfig):
    """Describe general class form by apps."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bboard'
