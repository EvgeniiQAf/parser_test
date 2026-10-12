"""CSV exporter for product data."""

import csv
import json
from pathlib import Path
from typing import Any

from models.product_data import Product

CSV_FIELDNAMES = [
    "title",
    "manufacturer",
    "color",
    "memory",
    "regular_price",
    "sale_price",
    "images",
    "product_code",
    "review_count",
    "screen_diagonal",
    "screen_resolution",
    "characteristics",
]


class CsvExporter:
    """Exports parsed Product dataclass instances to a CSV file."""

    def __init__(self, output_path: str | Path = "output/products.csv") -> None:
        self.output_path = Path(output_path)

    @staticmethod
    def serialize_product(product: Product) -> dict[str, Any]:
        """Convert a Product instance into a dictionary suitable for CSV."""
        return {
            "title": product.title,
            "manufacturer": product.manufacturer,
            "color": product.color,
            "memory": product.memory,
            "regular_price": product.regular_price,
            "sale_price": product.sale_price,
            "images": json.dumps(product.images, ensure_ascii=False),
            "product_code": product.product_code,
            "review_count": product.review_count,
            "screen_diagonal": product.screen_diagonal,
            "screen_resolution": product.screen_resolution,
            "characteristics": json.dumps(
                product.characteristics, ensure_ascii=False
            ),
        }

    def export(
        self,
        products: Product | list[Product],
        append: bool = True,
    ) -> Path:
        """Write product or list of products to the configured CSV file path."""
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        items = [products] if isinstance(products, Product) else products
        file_exists = self.output_path.exists()
        write_header = (
            not file_exists
            or not append
            or self.output_path.stat().st_size == 0
        )
        mode = "a" if append else "w"

        with open(
            self.output_path,
            mode=mode,
            newline="",
            encoding="utf-8-sig",
        ) as file:
            writer = csv.DictWriter(file, fieldnames=CSV_FIELDNAMES)
            if write_header:
                writer.writeheader()
            for product in items:
                writer.writerow(self.serialize_product(product))

        return self.output_path
