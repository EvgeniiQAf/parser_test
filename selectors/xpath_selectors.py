# XPath selectors for Selenium and Playwright.
XPATH_SELECTORS = {
    'title': '//h1[@class="main-title"]',
    'manufacturer': '//span[normalize-space()="Виробник"]/following-sibling::span',
    'color': (
        '//div[contains(@class, "current-product-series")]'
        '/following-sibling::div[contains(@class, "stuff-series-colors")]'
        '//div[contains(@class, "series-color") and contains(@class, "current")]'
    ),
    'memory': (
        '//div[contains(@class, "current-product-series")]'
        '//div[contains(@class, "current")]//a'
    ),
    'regular_price': (
        '//div[contains(@class, "main-price-block")]'
        '//div[@class="price-wrapper"]'
    ),
    'sale_price': None,
    'images': '//img[@id="product_main_image"]',
    'product_code': (
        '//div[@id="fast-navigation-block-static"]'
        '//span[@class="br-pr-code-val"]'
    ),
    'review_count': (
        '//div[@id="fast-navigation-block-static"]'
        '//li[@class="scroll-to-reviews"]/a'
    ),
    'screen_diagonal': (
        '//span[normalize-space()="Діагональ екрану"]'
        '/following-sibling::span//a'
    ),
    'screen_resolution': (
        '//a[starts-with(@title, "Роздільна здатність екрану")]'
    ),
    'characteristics_container': (
        '//div[@id="br-pr-7"]//div[@class="br-pr-chr"]'
    ),
    'characteristic_row': (
        '//div[@id="br-pr-7"]'
        '//div[@class="br-pr-chr-item"]/div/div'
    ),
    'characteristic_name': (
        '//div[@id="br-pr-7"]'
        '//div[@class="br-pr-chr-item"]/div/div'
        '/span[not(preceding-sibling::span)]'
    ),
    'characteristic_value': (
        '//div[@id="br-pr-7"]'
        '//div[@class="br-pr-chr-item"]/div/div'
        '/span[preceding-sibling::span]'
    ),

    # Additional elements for browser navigation.
    'search_input': (
        '//div[contains(@class, "header-top-in")]'
        '//div[contains(@class, "header-search-form")]'
        '//input[@type="search"]'
    ),
    'search_button': (
        '//div[contains(@class, "header-top-in")]'
        '//div[contains(@class, "header-search-form")]'
        '//input[@type="submit"]'
    ),
    'first_search_result': (
        '(//div[contains(@class, "product-wrapper")]'
        '//div[contains(@class, "br-pp-ipd-shown")]'
        '//a[@href])[1]'
    ),
}