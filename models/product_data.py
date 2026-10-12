"""Product data model."""

from dataclasses import dataclass, field
from typing import Self


def match_characteristic(specs: dict[str, str], *names: str) -> str | None:
    """Find a characteristic value by checking alias keys in normalized form."""
    expected = {name.casefold().replace("’", "'").strip() for name in names}
    for key, val in specs.items():
        if key.casefold().replace("’", "'").strip() in expected:
            return val
    return None


@dataclass
class Product:
    """Store parsed product information."""

    title: str | None = None
    manufacturer: str | None = None
    color: str | None = None
    memory: str | None = None
    regular_price: float | None = None
    sale_price: float | None = None
    images: list[str] = field(default_factory=list)
    product_code: str | None = None
    review_count: int | None = None
    screen_diagonal: str | None = None
    screen_resolution: str | None = None
    characteristics: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_raw(
        cls,
        specs: dict[str, str] | None = None,
        title: str | None = None,
        regular_price: float | None = None,
        sale_price: float | None = None,
        images: list[str] | None = None,
        product_code: str | None = None,
        review_count: int | None = None,
        manufacturer: str | None = None,
        color: str | None = None,
        memory: str | None = None,
        screen_diagonal: str | None = None,
        screen_resolution: str | None = None,
    ) -> Self:
        """Create a Product instance extracting core fields from specs."""
        specs_dict = specs or {}
        return cls(
            title=title,
            manufacturer=(
                manufacturer
                or match_characteristic(specs_dict, "Виробник", "Бренд")
            ),
            color=(
                color
                or match_characteristic(specs_dict, "Колір", "Колір корпусу")
            ),
            memory=(
                memory
                or match_characteristic(
                    specs_dict,
                    "Вбудована пам'ять",
                    "Об'єм вбудованої пам'яті",
                )
            ),
            regular_price=regular_price,
            sale_price=sale_price,
            images=images or [],
            product_code=product_code,
            review_count=review_count,
            screen_diagonal=(
                screen_diagonal
                or match_characteristic(specs_dict, "Діагональ екрану")
            ),
            screen_resolution=(
                screen_resolution
                or match_characteristic(
                    specs_dict, "Роздільна здатність екрану"
                )
            ),
            characteristics=specs_dict,
        )
