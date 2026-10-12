"""Selectors package for Brain.ua web scraping."""

from scraper.selectors.navigation import (
    NAVIGATION_SELECTORS,
    NAVIGATION_XPATH_SELECTORS,
)
from scraper.selectors.phone_css import (
    BS4_SELECTORS,
    PHONE_CSS_SELECTORS,
)
from scraper.selectors.phone_xpath import (
    CHARACTERISTIC_BASE,
    PHONE_XPATH_SELECTORS,
    PRICE_BASE,
    PRODUCT_XPATH_SELECTORS,
)

__all__ = [
    "BS4_SELECTORS",
    "CHARACTERISTIC_BASE",
    "NAVIGATION_SELECTORS",
    "NAVIGATION_XPATH_SELECTORS",
    "PHONE_CSS_SELECTORS",
    "PHONE_XPATH_SELECTORS",
    "PRICE_BASE",
    "PRODUCT_XPATH_SELECTORS",
]
