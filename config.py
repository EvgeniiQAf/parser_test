"""Configuration settings for Brain.ua parsers."""

# Base site URL
BASE_URL = "https://brain.com.ua/"

# Requests parser configuration (direct product URL)
PRODUCT_URL = (
    "https://brain.com.ua/ukr/"
    "Mobilniy_telefon_Apple_iPhone_16_Pro_Max_256GB_"
    "Black_Titanium-p1145443.html"
)

# Selenium parser configuration
SELENIUM_SEARCH_TEXT = "Apple iPhone 15 Pro 256GB Black"

# Playwright parser configuration
PLAYWRIGHT_SEARCH_TEXT = "Apple iPhone 16 PRO 256GB Black"
PLAYWRIGHT_EXPECTED_TITLE_PARTS = ("iphone 16 PRO", "256gb", "black")
