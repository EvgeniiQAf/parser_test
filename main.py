"""CLI entry point for Brain.ua product parsers."""

import argparse
import sys
from pathlib import Path

from rich.console import Console

from exporters.csv_exporter import CsvExporter
from parsers import (
    BaseParser,
    PlaywrightParser,
    RequestsParser,
    SeleniumParser,
)
from services.product_database_service import ProductDatabaseService
from services.product_service import ProductDisplayService

console = Console()

PARSER_REGISTRY: dict[str, type[BaseParser]] = {
    "selenium": SeleniumParser,
    "requests": RequestsParser,
    "playwright": PlaywrightParser,
}


def build_argument_parser() -> argparse.ArgumentParser:
    """Configure CLI arguments for parser and export options."""
    parser = argparse.ArgumentParser(
        description="Scrape Brain.ua product details using different engines."
    )
    parser.add_argument(
        "--parser",
        choices=list(PARSER_REGISTRY.keys()),
        default="selenium",
        help="Choose parser engine to run (default: selenium).",
    )
    parser.add_argument(
        "--csv",
        action="store_true",
        help="Export parsed product to a CSV file.",
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
        help="Save parsed product to the database via Django ORM.",
    )
    return parser


def run(
    parser_class: type[BaseParser],
    export_csv: bool = False,
    csv_path: str = "output/products.csv",
    save_db: bool = False,
) -> None:
    """Execute parser, display result, and optionally save to CSV or DB."""
    display = ProductDisplayService(console=console)
    with parser_class() as parser:
        product = parser.parse()

    display.display(product, title=f"{parser.name.upper()} PRODUCT")

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

    parser_class = PARSER_REGISTRY.get(args.parser)
    if not parser_class:
        arg_parser.print_help()
        sys.exit(1)

    run(
        parser_class=parser_class,
        export_csv=args.csv,
        csv_path=args.csv_path,
        save_db=args.db,
    )


if __name__ == "__main__":
    main()
