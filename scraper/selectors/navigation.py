"""Navigation and search XPath selectors for Brain.ua."""

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

# Semantic alias
NAVIGATION_SELECTORS = NAVIGATION_XPATH_SELECTORS

__all__ = ["NAVIGATION_SELECTORS", "NAVIGATION_XPATH_SELECTORS"]
