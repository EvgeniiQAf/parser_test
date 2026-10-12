"""Base parser abstract class defining the contract for all Brain.ua parsers."""

from abc import ABC, abstractmethod
from typing import Self

from models.product_data import Product


class BaseParser(ABC):
    """Abstract base class that all site parsers must implement."""

    name: str = "BaseParser"

    @abstractmethod
    def parse(self) -> Product:
        """Parse product information and return a populated Product instance."""

    def close(self) -> None:
        """Release any open resources. Subclasses may override this hook."""
        return None

    def __enter__(self) -> Self:
        """Support context manager protocol."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Ensure resources are cleanly closed on context exit."""
        self.close()
