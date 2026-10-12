"""Brain.ua product parser using Playwright with stealth evasions."""

import traceback
from pathlib import Path
from urllib.parse import urljoin

from playwright.sync_api import (
    BrowserContext,
    Page,
    Playwright,
    sync_playwright,
)
from playwright_stealth import Stealth

from models.product_data import Product
from parsers.base_parser import BaseParser
from parsers.helpers import (
    clean_text,
    parse_number,
    parse_price,
)
from product_selectors.xpath_selectors import (
    NAVIGATION_XPATH_SELECTORS,
    PRODUCT_XPATH_SELECTORS,
)
from services.product_service import ProductDisplayService

BASE_URL = "https://brain.com.ua/"
SEARCH_TEXT = "Apple iPhone 15 128GB Black"
EXPECTED_TITLE_PARTS = ("iphone 15", "128gb", "black")
WAIT_MS = 30_000
INSPECTION_MS = 5_000
STEP_DELAY_MS = 3_000
DEBUG_HTML = Path("brain_playwright_debug.html")
PROFILE_DIR = Path(".playwright_chrome_profile").resolve()


class PlaywrightParser(BaseParser):
    """Product parser based on Playwright Chromium and stealth plugin."""

    name = "Playwright"

    def __init__(
        self,
        base_url: str = BASE_URL,
        search_text: str = SEARCH_TEXT,
        expected_title_parts: tuple[str, ...] = EXPECTED_TITLE_PARTS,
        wait_ms: int = WAIT_MS,
        step_delay_ms: int = STEP_DELAY_MS,
        profile_dir: Path = PROFILE_DIR,
        headless: bool = False,
    ) -> None:
        self.base_url = base_url
        self.search_text = search_text
        self.expected_title_parts = expected_title_parts
        self.wait_ms = wait_ms
        self.step_delay_ms = step_delay_ms
        self.profile_dir = profile_dir
        self.headless = headless

        self._playwright_mgr = None
        self._playwright: Playwright | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None

    def start(self) -> None:
        """Start Playwright runtime and open browser context."""
        if self.context is not None:
            return

        self._playwright_mgr = sync_playwright()
        self._playwright = self._playwright_mgr.__enter__()

        self.context = self._playwright.chromium.launch_persistent_context(
            user_data_dir=str(self.profile_dir),
            headless=self.headless,
            locale="uk-UA",
            viewport={"width": 1440, "height": 900},
        )
        self.page = (
            self.context.pages[0]
            if self.context.pages
            else self.context.new_page()
        )
        self.page.set_default_timeout(self.wait_ms)
        Stealth().apply_stealth_sync(self.page)

    def close(self) -> None:
        """Close browser context and stop Playwright runtime cleanly."""
        if self.context is not None:
            try:
                self.context.close()
            except Exception:
                pass
            finally:
                self.context = None
                self.page = None

        if self._playwright_mgr is not None:
            try:
                self._playwright_mgr.__exit__(None, None, None)
            except Exception:
                pass
            finally:
                self._playwright_mgr = None
                self._playwright = None

    def _locator(self, xpath: str):
        if self.page is None:
            raise RuntimeError("Page is not initialized.")
        return self.page.locator(f"xpath={xpath}")

    def _text_of(self, locator) -> str | None:
        raw = locator.text_content(timeout=5_000) or ""
        return clean_text(raw)

    def _first_text(self, xpath: str | None) -> str | None:
        if not xpath or self.page is None:
            return None
        loc = self._locator(xpath)
        for idx in range(loc.count()):
            val = self._text_of(loc.nth(idx))
            if val:
                return val
        return None

    def _pause(self, msg: str) -> None:
        if self.page is not None and self.step_delay_ms > 0:
            self.page.wait_for_timeout(self.step_delay_ms)

    def expand_characteristics(self) -> None:
        """Ensure the technical specs accordion section is opened."""
        btn_loc = self._locator(
            PRODUCT_XPATH_SELECTORS["characteristics_button"]
        )
        if btn_loc.count() == 0:
            return
        btn = btn_loc.first
        classes = (btn.get_attribute("class") or "").split()
        if "open" not in classes:
            btn.scroll_into_view_if_needed()
            btn.click(timeout=10_000)

    def parse_characteristics(self) -> dict[str, str]:
        """Extract product characteristics key-value dictionary."""
        result: dict[str, str] = {}
        row_loc = self._locator(PRODUCT_XPATH_SELECTORS["characteristic_row"])

        for idx in range(row_loc.count()):
            spans = row_loc.nth(idx).locator("xpath=./span")
            if spans.count() < 2:
                continue
            name = self._text_of(spans.nth(0))
            value = self._text_of(spans.nth(1))
            if name and value:
                result[name.rstrip(":")] = value

        return result

    def parse_images(self) -> list[str]:
        """Extract unique large product images."""
        if self.page is None:
            return []
        images: list[str] = []
        loc = self._locator(PRODUCT_XPATH_SELECTORS["images"])
        attrs = (
            "data-observe-src",
            "data-zoom-image",
            "data-large",
            "data-src",
            "src",
        )

        for idx in range(loc.count()):
            elem = loc.nth(idx)
            for attr in attrs:
                url = elem.get_attribute(attr)
                if not url or url.startswith("data:"):
                    continue
                absolute = urljoin(self.page.url, url)
                if "/static/images/prod_img/" not in absolute:
                    continue
                if "small" in absolute.lower():
                    continue
                if absolute not in images:
                    images.append(absolute)
                break

        return images

    def parse_prices(self) -> tuple[float | None, float | None]:
        """Extract regular and sale prices."""
        sel = PRODUCT_XPATH_SELECTORS
        old_price = parse_price(self._first_text(sel["old_price"]))
        new_price = parse_price(self._first_text(sel["new_price"]))
        def_price = parse_price(self._first_text(sel["regular_price"]))

        if old_price and new_price and old_price > new_price:
            return old_price, new_price
        if old_price and def_price and old_price > def_price:
            return old_price, def_price
        return def_price or old_price or new_price, None

    def extract_product(self) -> Product:
        """Extract all details from currently loaded product page."""
        sel = PRODUCT_XPATH_SELECTORS
        regular, sale = self.parse_prices()
        reviews = parse_number(self._first_text(sel["review_count"]))

        return Product.from_raw(
            specs=self.parse_characteristics(),
            title=self._first_text(sel["title"]),
            regular_price=regular,
            sale_price=sale,
            images=self.parse_images(),
            product_code=self._first_text(sel["product_code"]),
            review_count=reviews,
            manufacturer=self._first_text(sel["manufacturer"]),
            color=self._first_text(sel["color"]),
            memory=self._first_text(sel["memory"]),
            screen_diagonal=self._first_text(sel["screen_diagonal"]),
            screen_resolution=self._first_text(sel["screen_resolution"]),
        )

    def parse(self) -> Product:
        """Execute full navigation flow, search, and extract product data."""
        self.start()
        page = self.page
        if page is None:
            raise RuntimeError("Page is not available.")

        page.goto(self.base_url, wait_until="domcontentloaded")
        self._pause("Home page loaded")

        search_input = (
            self._locator(NAVIGATION_XPATH_SELECTORS["search_input"])
            .filter(visible=True)
            .first
        )
        search_input.wait_for(state="visible", timeout=self.wait_ms)
        search_input.fill(self.search_text)
        self._pause("Search query entered")
        search_input.press("Enter")
        self._pause("Search submitted")

        target = (
            self._locator(NAVIGATION_XPATH_SELECTORS["target_search_result"])
            .filter(visible=True)
            .first
        )
        target.wait_for(state="visible", timeout=self.wait_ms)
        href = target.get_attribute("href")
        if not href:
            raise ValueError("Target result has no href attribute.")

        product_url = urljoin(page.url, href)
        self._pause("Matching result found")

        page.goto(product_url, wait_until="domcontentloaded")
        self._pause("Product page loaded")

        title_loc = self._locator(PRODUCT_XPATH_SELECTORS["title"]).first
        title_loc.wait_for(state="attached", timeout=self.wait_ms)
        title = self._text_of(title_loc) or ""
        norm_title = title.casefold().replace(" ", "")

        expected = [p.replace(" ", "") for p in self.expected_title_parts]
        if not all(p in norm_title for p in expected):
            raise ValueError(f"Wrong product loaded: {title!r} at {page.url}")

        chr_container = self._locator(
            PRODUCT_XPATH_SELECTORS["characteristics_container"]
        )
        if chr_container.count():
            chr_container.first.scroll_into_view_if_needed()

        self.expand_characteristics()
        self._pause("Characteristics expanded")

        self._locator(
            PRODUCT_XPATH_SELECTORS["characteristic_row"]
        ).first.wait_for(state="attached")

        self._pause("Before collecting product details")
        return self.extract_product()


def main() -> None:
    """Run PlaywrightParser standalone."""
    display = ProductDisplayService()
    parser = PlaywrightParser()
    try:
        product = parser.parse()
        display.display(product, title="PLAYWRIGHT PRODUCT")
    except Exception:
        traceback.print_exc()
    finally:
        parser.close()


if __name__ == "__main__":
    main()
