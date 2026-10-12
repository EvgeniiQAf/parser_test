# CSS product_selectors for Requests + BeautifulSoup.
BS4_SELECTORS = {
    'title': 'h1.main-title',
    'manufacturer': '.br-pr-chr-item > div > div > span:first-of-type + span',
    'color': '.current-product-series + .stuff-series-colors .series-color.current',
    'memory': '.current-product-series .series-characteristic.current a',
    'regular_price': '.main-price-block .price-wrapper',
    'sale_price': None,
    'images': '#product_main_image',
    'product_code': '#fast-navigation-block-static .br-pr-code-val',
    'review_count': '#fast-navigation-block-static .scroll-to-reviews a',
    'screen_diagonal': '.br-pr-chr-item a[title^="Діагональ екрану"]',
    'screen_resolution': '.br-pr-chr-item a[title^="Роздільна здатність екрану"]',
    'characteristics_container': '#br-pr-7 .br-pr-chr',
    'characteristic_row': '#br-pr-7 .br-pr-chr-item > div > div',
    'characteristic_name': '#br-pr-7 .br-pr-chr-item > div > div > span:first-of-type',
    'characteristic_value': '#br-pr-7 .br-pr-chr-item > div > div > span ~ span',
}
