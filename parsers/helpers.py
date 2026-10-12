"""Common text and data parsing helper functions for Brain.ua parsers."""

import re

from models.product_data import match_characteristic


def clean_text(value: str | None) -> str | None:
    """Normalize whitespace and strip text, returning None if empty."""
    if not value:
        return None
    normalized = " ".join(value.split())
    return normalized or None


def parse_number(value: str | None) -> int | None:
    """Extract integer value from a string containing digits."""
    if not value:
        return None
    match = re.search(r"\d+", value.replace(" ", ""))
    return int(match.group()) if match else None


def parse_price(value: str | None) -> float | None:
    """Extract price float from raw string (e.g. '53 999 грн' -> 53999.0)."""
    if not value:
        return None
    match = re.search(r"\d[\d\s\u00a0]*(?:[,.]\d{1,2})?", value)
    if not match:
        return None
    cleaned = re.sub(r"\s", "", match.group()).replace(",", ".")
    try:
        return float(cleaned)
    except ValueError:
        return None


__all__ = [
    "clean_text",
    "match_characteristic",
    "parse_number",
    "parse_price",
]
