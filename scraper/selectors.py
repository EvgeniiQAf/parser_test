"""Selectors for Brain.ua scrapers (XPath and CSS)."""

CHARACTERISTIC_BASE = (
    "//div[@id='br-pr-7']//div[contains(@class, 'br-pr-chr-item')]"
)
PRICE_BASE = "//div[contains(@class, 'main-price-block')]"

PRODUCT_XPATH_SELECTORS = {
    "title": "//h1[contains(@class, 'main-title')]",
    "manufacturer": (
        CHARACTERISTIC_BASE
        + "//span[normalize-space()='Виробник']/following-sibling::span[1]"
    ),
    "color": (
        CHARACTERISTIC_BASE
        + "//span[normalize-space()='Колір']/following-sibling::span[1]"
    ),
    "memory": (
        CHARACTERISTIC_BASE
        + '//span[normalize-space()="Вбудована пам\'ять"]/following-sibling::span[1]'
    ),
    "regular_price": PRICE_BASE + "//*[contains(@class, 'price-wrapper')]",
    "sale_price": (
        PRICE_BASE
        + "//*[contains(@class, 'new-price') or contains(@class, 'sale-price')]"
    ),
    "old_price": (
        PRICE_BASE
        + "//*[contains(@class, 'old-price') or contains(@class, 'price-old')]"
    ),
    "new_price": (
        PRICE_BASE
        + "//*[contains(@class, 'new-price')"
        + " or contains(@class, 'sale-price')"
        + " or contains(@class, 'red-price')]"
    ),
    "images": (
        "//img[@id='product_main_image']"
        " | //*[contains(@class, 'br-pr') and "
        "(contains(@class, 'gallery') or contains(@class, 'slider') "
        "or contains(@class, 'thumb'))]//img"
    ),
    "product_code": "//span[contains(@class, 'br-pr-code-val')]",
    "review_count": "//li[contains(@class, 'scroll-to-reviews')]//a",
    "screen_diagonal": (
        CHARACTERISTIC_BASE
        + "//span[normalize-space()='Діагональ екрану']/following-sibling::span[1]"
    ),
    "screen_resolution": (
        CHARACTERISTIC_BASE
        + "//span[normalize-space()='Роздільна здатність екрану']"
        + "/following-sibling::span[1]"
    ),
    "characteristics_container": (
        "//div[@id='br-pr-7']//div[contains(@class, 'br-pr-chr')]"
    ),
    "characteristics_button": (
        "//div[@id='br-pr-7']//button[contains(@class, 'br-prs-button')]"
    ),
    "characteristic_row": CHARACTERISTIC_BASE + "/div/div",
    "characteristic_name": CHARACTERISTIC_BASE + "/div/div/span[1]",
    "characteristic_value": CHARACTERISTIC_BASE + "/div/div/span[position()>1]",
}

NAVIGATION_XPATH_SELECTORS = {
    "search_input": "//input[@type='search']",
    "search_button": (
        "//div[contains(@class, 'header-search-form')]//input[@type='submit']"
    ),
    "first_search_result": (
        "(//div[contains(@class, 'view-grid') or contains(@class, 'search-wrapper')]"
        "//div[contains(@class, 'br-pp-img')]//a[img])[1]"
    ),
    "search_results": (
        "//div[contains(@class, 'view-grid') or contains(@class, 'search-wrapper')]"
        "//div[contains(@class, 'br-pp-img')]//a[img]"
    ),
}

BS4_SELECTORS = {
    "title": "h1.main-title",
    "manufacturer": ".br-pr-chr-item > div > div > span:first-of-type + span",
    "color": ".current-product-series + .stuff-series-colors .series-color.current",
    "memory": ".current-product-series .series-characteristic.current a",
    "regular_price": ".main-price-block .price-wrapper",
    "sale_price": None,
    "images": "#product_main_image",
    "product_code": "#fast-navigation-block-static .br-pr-code-val",
    "review_count": "#fast-navigation-block-static .scroll-to-reviews a",
    "screen_diagonal": '.br-pr-chr-item a[title^="Діагональ екрану"]',
    "screen_resolution": '.br-pr-chr-item a[title^="Роздільна здатність екрану"]',
    "characteristics_container": "#br-pr-7 .br-pr-chr",
    "characteristic_row": "#br-pr-7 .br-pr-chr-item > div > div",
    "characteristic_name": "#br-pr-7 .br-pr-chr-item > div > div > span:first-of-type",
    "characteristic_value": "#br-pr-7 .br-pr-chr-item > div > div > span ~ span",
}

__all__ = [
    "BS4_SELECTORS",
    "CHARACTERISTIC_BASE",
    "NAVIGATION_XPATH_SELECTORS",
    "PRICE_BASE",
    "PRODUCT_XPATH_SELECTORS",
]
