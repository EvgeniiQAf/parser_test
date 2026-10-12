"""Brain.ua product scraper using Selenium and undetected_chromedriver."""

import time
import traceback
from pathlib import Path
from urllib.parse import urljoin

import undetected_chromedriver as uc
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from config import BASE_URL, SELENIUM_SEARCH_TEXT
from scraper.display import ProductDisplayService
from scraper.engines.base_scraper import BaseScraper
from scraper.models import ScrapedProduct
from scraper.selectors import (
    NAVIGATION_XPATH_SELECTORS,
    PRODUCT_XPATH_SELECTORS,
)
from scraper.utils import (
    clean_text,
    parse_number,
    parse_price,
)

CHROME_VERSION = 154
WAIT_SECONDS = 30
INSPECTION_SECONDS = 5
DEBUG_HTML = Path("brain_product_debug.html")


class SeleniumScraper(BaseScraper):
    """Product scraper based on undetected_chromedriver (Selenium)."""

    name = "Selenium"

    def __init__(
        self,
        base_url: str = BASE_URL,
        search_text: str = SELENIUM_SEARCH_TEXT,
        chrome_version: int = CHROME_VERSION,
        wait_seconds: int = WAIT_SECONDS,
        headless: bool = False,
    ) -> None:
        self.base_url = base_url
        self.search_text = search_text
        self.chrome_version = chrome_version
        self.wait_seconds = wait_seconds
        self.headless = headless
        self.driver: uc.Chrome | None = None

    def _init_driver(self) -> uc.Chrome:
        """Create and configure undetected_chromedriver instance."""
        options = uc.ChromeOptions()
        options.add_argument("--no-first-run")
        options.add_argument("--no-default-browser-check")
        return uc.Chrome(
            options=options,
            version_main=self.chrome_version,
            headless=self.headless,
        )

    def start(self) -> None:
        """Initialize the browser driver if not already open."""
        if self.driver is None:
            self.driver = self._init_driver()

    def close(self) -> None:
        """Safely quit browser session and free resources."""
        if self.driver is not None:
            try:
                self.driver.quit()
            except WebDriverException:
                pass
            finally:
                self.driver = None

    def _text_of(self, element) -> str | None:
        if element is None:
            return None
        raw = element.text or element.get_attribute("textContent") or ""
        return clean_text(raw)

    def _first_text(self, xpath: str | None) -> str | None:
        if not xpath or self.driver is None:
            return None
        for element in self.driver.find_elements(By.XPATH, xpath):
            text = self._text_of(element)
            if text:
                return text
        return None

    def _visible_element(self, xpath: str):
        if self.driver is None:
            return None
        for element in self.driver.find_elements(By.XPATH, xpath):
            if element.is_displayed():
                return element
        return None

    def expand_characteristics(self) -> None:
        """Open the specifications section if currently collapsed."""
        if self.driver is None:
            return
        xpath = PRODUCT_XPATH_SELECTORS["characteristics_button"]
        buttons = self.driver.find_elements(By.XPATH, xpath)
        if not buttons:
            return
        button = buttons[0]
        classes = (button.get_attribute("class") or "").split()
        if "open" not in classes:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", button
            )
            self.driver.execute_script("arguments[0].click();", button)

    def parse_characteristics(self) -> dict[str, str]:
        """Extract product characteristics into key-value pairs."""
        if self.driver is None:
            return {}
        characteristics: dict[str, str] = {}
        xpath = PRODUCT_XPATH_SELECTORS["characteristic_row"]
        rows = self.driver.find_elements(By.XPATH, xpath)

        for row in rows:
            spans = row.find_elements(By.XPATH, "./span")
            if len(spans) < 2:
                continue
            name = self._text_of(spans[0])
            value = self._text_of(spans[1])
            if name and value:
                characteristics[name.rstrip(":")] = value

        return characteristics

    def parse_images(self) -> list[str]:
        """Extract unique large product images."""
        if self.driver is None:
            return []
        images: list[str] = []
        xpath = PRODUCT_XPATH_SELECTORS["images"]

        for element in self.driver.find_elements(By.XPATH, xpath):
            for attr in (
                "data-observe-src",
                "data-zoom-image",
                "data-large",
                "data-src",
                "src",
            ):
                url = element.get_attribute(attr)
                if not url or url.startswith("data:"):
                    continue

                absolute = urljoin(self.driver.current_url, url)
                if "/static/images/prod_img/" not in absolute:
                    continue
                if "small" in absolute.lower():
                    continue
                if absolute not in images:
                    images.append(absolute)
                break

        return images

    def parse_prices(self) -> tuple[float | None, float | None]:
        """Extract regular and sale prices from product page markup."""
        old_xpath = PRODUCT_XPATH_SELECTORS["old_price"]
        new_xpath = PRODUCT_XPATH_SELECTORS["new_price"]
        reg_xpath = PRODUCT_XPATH_SELECTORS.get("regular_price")

        old_price = parse_price(self._first_text(old_xpath))
        new_price = parse_price(self._first_text(new_xpath))
        def_price = parse_price(self._first_text(reg_xpath))

        if old_price and new_price and old_price > new_price:
            return old_price, new_price
        if old_price and def_price and old_price > def_price:
            return old_price, def_price
        return def_price or old_price or new_price, None

    def extract_product(self) -> ScrapedProduct:
        """Extract all details from currently loaded product page."""
        selectors = PRODUCT_XPATH_SELECTORS
        regular, sale = self.parse_prices()
        reviews = parse_number(self._first_text(selectors.get("review_count")))

        return ScrapedProduct.from_raw(
            specs=self.parse_characteristics(),
            title=self._first_text(selectors.get("title")),
            regular_price=regular,
            sale_price=sale,
            images=self.parse_images(),
            product_code=self._first_text(selectors.get("product_code")),
            review_count=reviews,
            manufacturer=self._first_text(selectors.get("manufacturer")),
            color=self._first_text(selectors.get("color")),
            memory=self._first_text(selectors.get("memory")),
            screen_diagonal=self._first_text(selectors.get("screen_diagonal")),
            screen_resolution=self._first_text(
                selectors.get("screen_resolution")
            ),
        )

    def parse(self) -> ScrapedProduct:
        """Navigate to site, search product, and extract all details."""
        self.start()
        driver = self.driver
        if driver is None:
            raise RuntimeError("WebDriver failed to initialize.")

        wait = WebDriverWait(driver, self.wait_seconds)
        if driver.window_handles:
            driver.switch_to.window(driver.window_handles[0])
        driver.get(self.base_url)

        search_xpath = NAVIGATION_XPATH_SELECTORS["search_input"]
        search = wait.until(lambda d: self._visible_element(search_xpath))
        search.send_keys(self.search_text)
        search.send_keys(Keys.ENTER)

        wait.until(
            lambda d: "/search/" in d.current_url or "Search=" in d.current_url
        )

        first_xpath = NAVIGATION_XPATH_SELECTORS["first_search_result"]
        first_result = wait.until(lambda d: self._visible_element(first_xpath))

        target_el = first_result
        keywords = [
            w.casefold()
            for w in self.search_text.split()
            if len(w) > 2
            and w.casefold() not in ("apple", "мобільний", "телефон")
        ]
        if keywords:
            cards = driver.find_elements(
                By.XPATH, NAVIGATION_XPATH_SELECTORS["search_results"]
            )
            for card in cards[:12]:
                if not card.is_displayed():
                    continue
                href = (card.get_attribute("href") or "").casefold().replace(
                    "_", ""
                )
                if all(k in href for k in keywords):
                    target_el = card
                    break

        target_el.click()

        title_xpath = PRODUCT_XPATH_SELECTORS["title"]
        wait.until(
            lambda d: "/search/" not in d.current_url
            and bool(d.find_elements(By.XPATH, title_xpath))
        )

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        self.expand_characteristics()
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.5)

        return self.extract_product()


# Backward compatibility alias
SeleniumParser = SeleniumScraper


def main() -> None:
    """Run SeleniumScraper standalone."""
    display = ProductDisplayService()
    scraper = SeleniumScraper()
    try:
        product = scraper.parse()
        display.display(product, title="SELENIUM SCRAPER")
    except Exception:
        traceback.print_exc()
    finally:
        scraper.close()


if __name__ == "__main__":
    main()
