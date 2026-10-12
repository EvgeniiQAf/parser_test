"""Brain.ua product scraper using HTTP requests and BeautifulSoup4."""

from urllib.parse import urljoin

from bs4 import BeautifulSoup
from curl_cffi import requests

from config import PRODUCT_URL
from scraper.display import ProductDisplayService
from scraper.engines.base_scraper import BaseScraper
from scraper.models import ScrapedProduct
from scraper.selectors import BS4_SELECTORS
from scraper.utils import clean_text, parse_number, parse_price


class RequestsScraper(BaseScraper):
    """Fast scraper based on curl_cffi requests and BeautifulSoup."""

    name = "Requests"

    def __init__(self, url: str = PRODUCT_URL, timeout: int = 20) -> None:
        self.url = url
        self.timeout = timeout

    def fetch_html(self, url: str) -> str:
        """Download product HTML using curl_cffi with Chrome impersonation."""
        response = requests.get(
            url,
            impersonate="chrome",
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.text

    def parse_characteristics(self, soup: BeautifulSoup) -> dict[str, str]:
        """Extract all product characteristics into a key-value mapping."""
        characteristics: dict[str, str] = {}
        rows = soup.select(BS4_SELECTORS["characteristic_row"])

        for row in rows:
            name_elem = row.select_one("span:first-of-type")
            value_elems = row.select("span ~ span")

            name = (
                clean_text(name_elem.get_text(" ", strip=True))
                if name_elem
                else None
            )
            values = [
                clean_text(elem.get_text(" ", strip=True))
                for elem in value_elems
            ]
            valid_values = [v for v in values if v]

            if name and valid_values:
                characteristics[name.rstrip(":")] = " ".join(valid_values)

        return characteristics

    def parse_images(self, soup: BeautifulSoup, base_url: str) -> list[str]:
        """Extract unique product images."""
        images: list[str] = []
        image_elements = soup.select(BS4_SELECTORS["images"])

        for image in image_elements:
            image_url = (
                image.get("data-src")
                or image.get("src")
                or image.get("href")
            )
            if not image_url:
                continue

            full_url = urljoin(base_url, image_url)
            if full_url not in images:
                images.append(full_url)

        return images

    def parse(self) -> ScrapedProduct:
        """Fetch page HTML and parse into a populated ScrapedProduct dataclass."""
        html = self.fetch_html(self.url)
        soup = BeautifulSoup(html, "lxml")

        specs = self.parse_characteristics(soup)

        title_elem = soup.select_one(BS4_SELECTORS["title"])
        title = (
            clean_text(title_elem.get_text(" ", strip=True))
            if title_elem
            else None
        )

        reg_elem = soup.select_one(BS4_SELECTORS["regular_price"])
        reg_text = (
            clean_text(reg_elem.get_text(" ", strip=True))
            if reg_elem
            else None
        )
        regular_price = parse_price(reg_text)

        sale_selector = BS4_SELECTORS.get("sale_price")
        sale_elem = soup.select_one(sale_selector) if sale_selector else None
        sale_text = (
            clean_text(sale_elem.get_text(" ", strip=True))
            if sale_elem
            else None
        )
        sale_price = parse_price(sale_text)

        code_elem = soup.select_one(BS4_SELECTORS["product_code"])
        code_text = (
            clean_text(code_elem.get_text(" ", strip=True))
            if code_elem
            else None
        )

        rev_elem = soup.select_one(BS4_SELECTORS["review_count"])
        rev_text = (
            clean_text(rev_elem.get_text(" ", strip=True))
            if rev_elem
            else None
        )
        review_count = parse_number(rev_text)

        return ScrapedProduct.from_raw(
            specs=specs,
            title=title,
            regular_price=regular_price,
            sale_price=sale_price,
            images=self.parse_images(soup, self.url),
            product_code=code_text,
            review_count=review_count,
        )


# Backward compatibility alias
RequestsParser = RequestsScraper


def main() -> None:
    """Run RequestsScraper standalone."""
    with RequestsScraper() as scraper:
        product = scraper.parse()
    ProductDisplayService().display(product, title="REQUESTS SCRAPER")


if __name__ == "__main__":
    main()
