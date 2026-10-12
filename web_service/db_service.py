"""Database persistence service for saving ScrapedProduct via Django ORM."""

import os
import sys
from decimal import Decimal
from pathlib import Path

# Ensure Django environment is configured
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_service.config.settings")

import django  # noqa: E402

django.setup()

from scraper.models import ScrapedProduct  # noqa: E402
from web_service.products.models import ProductModel  # noqa: E402


class ProductDatabaseService:
    """Handles persisting ScrapedProduct instances into database via Django ORM."""

    @staticmethod
    def save(product: ScrapedProduct) -> ProductModel:
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


__all__ = ["ProductDatabaseService"]
