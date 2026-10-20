"""Configure the authentication application."""

from django.apps import AppConfig


class AuthAppConfig(AppConfig):
    """Register the user management and authentication app."""

    name = "auth_app"