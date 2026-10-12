"""App configuration for products."""

from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """Application configuration for parsed products."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "web_service.products"
    verbose_name = "Товари Brain.ua"
