"""Service layer for terminal formatting and styled output using Rich."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from scraper.models import ScrapedProduct


class ProductDisplayService:
    """Handles formatted console presentation of ScrapedProduct models."""

    def __init__(self, console: Console | None = None) -> None:
        self.console = console or Console()

    def display(
        self,
        product: ScrapedProduct,
        title: str = "PRODUCT INFORMATION",
    ) -> None:
        """Render product details, image galleries, and specs in styled tables."""
        self.console.print()
        self.console.print(
            Panel(
                product.title or "Unknown product",
                title=title,
                border_style="cyan",
            )
        )

        self._print_general_info(product)
        self._print_images(product)
        self._print_characteristics(product)

    def _print_general_info(self, product: ScrapedProduct) -> None:
        info_table = Table(
            title="General Information",
            show_header=True,
            header_style="bold cyan",
            expand=True,
        )
        info_table.add_column("Field", style="bold", width=22)
        info_table.add_column("Value", overflow="fold")

        fields = [
            ("Manufacturer", product.manufacturer),
            ("Color", product.color),
            ("Memory", product.memory),
            ("Product code", product.product_code),
            ("Reviews", product.review_count),
            ("Screen diagonal", product.screen_diagonal),
            ("Screen resolution", product.screen_resolution),
            ("Regular price", product.regular_price),
            ("Sale price", product.sale_price),
        ]

        for name, value in fields:
            info_table.add_row(
                name,
                str(value) if value is not None else "—",
            )

        self.console.print(info_table)

    def _print_images(self, product: ScrapedProduct) -> None:
        images_table = Table(
            title=f"Product Images ({len(product.images)})",
            expand=True,
        )
        images_table.add_column("#", width=4)
        images_table.add_column("Image URL", overflow="fold")

        for index, image_url in enumerate(product.images, start=1):
            images_table.add_row(str(index), image_url)

        self.console.print(images_table)

    def _print_characteristics(self, product: ScrapedProduct) -> None:
        characteristics_table = Table(
            title=f"Characteristics ({len(product.characteristics)})",
            show_lines=True,
            expand=True,
        )
        characteristics_table.add_column(
            "Characteristic",
            style="cyan",
            ratio=1,
        )
        characteristics_table.add_column(
            "Value",
            ratio=2,
            overflow="fold",
        )

        for name, value in product.characteristics.items():
            characteristics_table.add_row(name, value)

        self.console.print(characteristics_table)


__all__ = ["ProductDisplayService"]
