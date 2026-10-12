"""Unit tests for Brain.ua parser helpers, data model, and CLI runner."""

import csv
import json
from pathlib import Path

import pytest

from exporters.csv_exporter import CSV_FIELDNAMES, CsvExporter
from main import PARSER_REGISTRY, build_argument_parser
from models.product_data import Product
from parsers.helpers import (
    clean_text,
    match_characteristic,
    parse_number,
    parse_price,
)


def test_clean_text() -> None:
    assert clean_text("  hello   world  ") == "hello world"
    assert clean_text("") is None
    assert clean_text(None) is None
    assert clean_text("   \n\t  ") is None


def test_parse_number() -> None:
    assert parse_number("12 відгуків") == 12
    assert parse_number("  450 ") == 450
    assert parse_number("без відгуків") is None
    assert parse_number(None) is None


def test_parse_price() -> None:
    assert parse_price("53 999 грн") == 53999.0
    assert parse_price("53\u00a0999,50 грн") == 53999.5
    assert parse_price("1 234.99") == 1234.99
    assert parse_price("Немає в наявності") is None
    assert parse_price(None) is None


def test_match_characteristic() -> None:
    specs = {
        "Виробник": "Apple",
        "Вбудована пам’ять": "128 ГБ",
        "Колір корпусу": "Black",
    }
    assert match_characteristic(specs, "Виробник", "Бренд") == "Apple"
    # Match with different apostrophe variation
    assert (
        match_characteristic(
            specs, "Вбудована пам'ять", "Об'єм вбудованої пам'яті"
        )
        == "128 ГБ"
    )
    assert match_characteristic(specs, "колір корпусу") == "Black"
    assert match_characteristic(specs, "Невідомо") is None


def test_product_model_defaults() -> None:
    product = Product()
    assert product.title is None
    assert product.images == []
    assert product.characteristics == {}

    # Check mutable default independence
    product.images.append("https://example.com/1.jpg")
    other_product = Product()
    assert other_product.images == []


def test_product_from_raw() -> None:
    specs = {
        "Виробник": "Apple",
        "Колір": "Black",
        "Вбудована пам'ять": "256 GB",
        "Діагональ екрану": "6.7",
        "Роздільна здатність екрану": "2796x1290",
    }
    product = Product.from_raw(
        specs=specs,
        title="iPhone 15 Pro",
        regular_price=49999.0,
    )
    assert product.title == "iPhone 15 Pro"
    assert product.manufacturer == "Apple"
    assert product.color == "Black"
    assert product.memory == "256 GB"
    assert product.screen_diagonal == "6.7"
    assert product.screen_resolution == "2796x1290"
    assert product.regular_price == 49999.0
    assert product.characteristics == specs


def test_cli_parser_registry() -> None:
    arg_parser = build_argument_parser()
    args_default = arg_parser.parse_args([])
    assert args_default.parser == "selenium"
    assert not args_default.csv
    assert not args_default.db
    assert args_default.csv_path == "output/products.csv"

    args_custom = arg_parser.parse_args(
        ["--parser", "requests", "--csv", "--db", "--csv-path", "custom.csv"]
    )
    assert args_custom.parser == "requests"
    assert args_custom.csv is True
    assert args_custom.db is True
    assert args_custom.csv_path == "custom.csv"
    assert "requests" in PARSER_REGISTRY

    with pytest.raises(SystemExit):
        arg_parser.parse_args(["--parser", "unsupported_engine"])


def test_csv_exporter_single_product(tmp_path: Path) -> None:
    csv_file = tmp_path / "test_products.csv"
    exporter = CsvExporter(output_path=csv_file)

    product = Product(
        title="Apple iPhone 15 128GB Black",
        manufacturer="Apple",
        regular_price=34999.0,
        images=["https://brain.com.ua/img1.jpg", "https://brain.com.ua/img2.jpg"],
        characteristics={"Колір": "Black", "Пам'ять": "128 ГБ"},
    )

    result_path = exporter.export(product)
    assert result_path == csv_file
    assert csv_file.exists()

    with open(csv_file, encoding="utf-8-sig") as file:
        reader = list(csv.DictReader(file))
        assert len(reader) == 1
        row = reader[0]
        assert row["title"] == "Apple iPhone 15 128GB Black"
        assert row["manufacturer"] == "Apple"
        assert float(row["regular_price"]) == 34999.0
        assert json.loads(row["images"]) == [
            "https://brain.com.ua/img1.jpg",
            "https://brain.com.ua/img2.jpg",
        ]
        assert json.loads(row["characteristics"]) == {
            "Колір": "Black",
            "Пам'ять": "128 ГБ",
        }


def test_csv_exporter_append_mode(tmp_path: Path) -> None:
    csv_file = tmp_path / "test_append.csv"
    exporter = CsvExporter(output_path=csv_file)

    product1 = Product(title="Product 1", regular_price=100.0)
    product2 = Product(title="Product 2", regular_price=200.0)

    exporter.export(product1, append=True)
    exporter.export(product2, append=True)

    with open(csv_file, encoding="utf-8-sig") as file:
        reader = list(csv.DictReader(file))
        assert len(reader) == 2
        assert reader[0]["title"] == "Product 1"
        assert reader[1]["title"] == "Product 2"
        assert list(reader[0].keys()) == CSV_FIELDNAMES


def test_product_database_service_save() -> None:
    from backend.products.models import ProductModel
    from services.product_database_service import ProductDatabaseService

    code = "TEST_UNIQUE_CODE_001"
    ProductModel.objects.filter(product_code=code).delete()

    product = Product(
        title="Test Phone",
        manufacturer="Test Brand",
        regular_price=1000.0,
        product_code=code,
        images=["https://example.com/test.jpg"],
        characteristics={"Test": "Value"},
    )

    db_item = ProductDatabaseService.save(product)
    assert db_item.id is not None
    assert db_item.title == "Test Phone"
    assert db_item.product_code == code
    assert float(db_item.regular_price) == 1000.0

    product.regular_price = 850.0
    updated_item = ProductDatabaseService.save(product)
    assert updated_item.id == db_item.id
    assert float(updated_item.regular_price) == 850.0
    assert ProductModel.objects.filter(product_code=code).count() == 1
    ProductModel.objects.filter(product_code=code).delete()
