"""CLI orchestrator entry point connecting Scraper and WebService modules."""

import argparse
import sys
from pathlib import Path

from rich.console import Console

from scraper import (
    BaseScraper,
    CsvExporter,
    PlaywrightScraper,
    ProductDisplayService,
    RequestsScraper,
    SeleniumScraper,
)
from web_service import ProductDatabaseService

console = Console()

SCRAPER_REGISTRY: dict[str, type[BaseScraper]] = {
    "selenium": SeleniumScraper,
    "requests": RequestsScraper,
    "playwright": PlaywrightScraper,
}

# Backward compatibility alias
PARSER_REGISTRY = SCRAPER_REGISTRY


def build_argument_parser() -> argparse.ArgumentParser:
    """Configure CLI arguments for scraper and export options."""
    parser = argparse.ArgumentParser(
        description="Scrape Brain.ua product details using different engines."
    )
    parser.add_argument(
        "--scraper",
        "--parser",
        dest="scraper",
        choices=list(SCRAPER_REGISTRY.keys()),
        default="selenium",
        help="Choose scraping engine to run (default: selenium).",
    )
    parser.add_argument(
        "--csv",
        action="store_true",
        help="Export scraped product to a CSV file.",
    )
    parser.add_argument(
        "--csv-path",
        type=str,
        default="output/products.csv",
        help="Destination path for CSV export (default: output/products.csv).",
    )
    parser.add_argument(
        "--db",
        action="store_true",
        help="Save scraped product to the database via Django ORM.",
    )
    return parser


def run(
    scraper_class: type[BaseScraper],
    export_csv: bool = False,
    csv_path: str = "output/products.csv",
    save_db: bool = False,
) -> None:
    """Execute scraper, display result, and optionally save to CSV or DB."""
    display = ProductDisplayService(console=console)
    with scraper_class() as scraper:
        product = scraper.parse()

    display.display(product, title=f"{scraper.name.upper()} PRODUCT")

    if export_csv:
        exporter = CsvExporter(output_path=Path(csv_path))
        saved_path = exporter.export(product)
        console.print(
            f"[bold green]✔ Successfully exported product to: {saved_path}[/]"
        )

    if save_db:
        db_product = ProductDatabaseService.save(product)
        console.print(
            "[bold green]✔ Successfully saved product to database "
            f"(ID: {db_product.id}, Code: {db_product.product_code})[/]"
        )


def main() -> None:
    """Main CLI handler."""
    arg_parser = build_argument_parser()
    args = arg_parser.parse_args()

    scraper_class = SCRAPER_REGISTRY.get(args.scraper)
    if not scraper_class:
        arg_parser.print_help()
        sys.exit(1)

    run(
        scraper_class=scraper_class,
        export_csv=args.csv,
        csv_path=args.csv_path,
        save_db=args.db,
    )


if __name__ == "__main__":
    main()
