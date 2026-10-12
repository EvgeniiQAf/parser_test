"""Admin dashboard registration for products."""

from django.contrib import admin

from backend.products.models import ProductModel


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    """Admin configuration for ProductModel."""

    list_display = (
        "product_code",
        "title",
        "manufacturer",
        "regular_price",
        "sale_price",
        "updated_at",
    )
    search_fields = (
        "title",
        "product_code",
        "manufacturer",
    )
    list_filter = (
        "manufacturer",
        "updated_at",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
