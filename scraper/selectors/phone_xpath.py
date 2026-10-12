"""XPath selectors for Brain.ua mobile phone product pages."""

CHARACTERISTIC_BASE = (
    "//div[@id='br-pr-7']//div[contains(@class, 'br-pr-chr-item')]"
)
PRICE_BASE = "//div[contains(@class, 'main-price-block')]"

PHONE_XPATH_SELECTORS = {
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

# Backward compatibility alias
PRODUCT_XPATH_SELECTORS = PHONE_XPATH_SELECTORS

__all__ = [
    "CHARACTERISTIC_BASE",
    "PHONE_XPATH_SELECTORS",
    "PRICE_BASE",
    "PRODUCT_XPATH_SELECTORS",
]
