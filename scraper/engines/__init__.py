"""Scraper engine implementations for Brain.ua."""

from scraper.engines.base_scraper import BaseParser, BaseScraper
from scraper.engines.playwright_scraper import PlaywrightParser, PlaywrightScraper
from scraper.engines.requests_scraper import RequestsParser, RequestsScraper
from scraper.engines.selenium_scraper import SeleniumParser, SeleniumScraper

__all__ = [
    "BaseParser",
    "BaseScraper",
    "PlaywrightParser",
    "PlaywrightScraper",
    "RequestsParser",
    "RequestsScraper",
    "SeleniumParser",
    "SeleniumScraper",
]
