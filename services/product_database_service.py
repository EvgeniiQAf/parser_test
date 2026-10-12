"""Database service for storing parsed products via Django ORM."""

from decimal import Decimal

import modules.load_django  # noqa: F401
from backend.products.models import ProductModel
from models.product_data import Product


class ProductDatabaseService:
    """Handles persisting Product instances into the database using Django ORM."""

    @staticmethod
    def save(product: Product) -> ProductModel:
        """Create or update a ProductModel record in the database."""
        regular_price = (
            Decimal(str(product.regular_price))
            if product.regular_price is not None
            else None
        )
        sale_price = (
            Decimal(str(product.sale_price))
            if product.sale_price is not None
            else None
        )

        defaults = {
            "title": product.title,
            "manufacturer": product.manufacturer,
            "color": product.color,
            "memory": product.memory,
            "regular_price": regular_price,
            "sale_price": sale_price,
            "images": product.images,
            "review_count": product.review_count,
            "screen_diagonal": product.screen_diagonal,
            "screen_resolution": product.screen_resolution,
            "characteristics": product.characteristics,
        }

        if product.product_code:
            obj, _ = ProductModel.objects.update_or_create(
                product_code=product.product_code,
                defaults=defaults,
            )
            return obj

        return ProductModel.objects.create(
            product_code=None,
            **defaults,
        )
