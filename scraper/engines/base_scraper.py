"""Base scraper abstract class defining the contract for all Brain.ua scrapers."""

from abc import ABC, abstractmethod
from typing import Self

from scraper.models import ScrapedProduct


class BaseScraper(ABC):
    """Abstract base class that all site scrapers must implement."""

    name: str = "BaseScraper"

    @abstractmethod
    def parse(self) -> ScrapedProduct:
        """Parse product information and return a populated ScrapedProduct instance."""

    def close(self) -> None:
        """Release any open resources. Subclasses may override this hook."""
        return None

    def __enter__(self) -> Self:
        """Support context manager protocol."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Ensure resources are cleanly closed on context exit."""
        self.close()


# Backward compatibility alias
BaseParser = BaseScraper

__all__ = ["BaseParser", "BaseScraper"]
