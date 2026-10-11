from pprint import pprint
import requests
from bs4 import BeautifulSoup
from models.product_data import create_product_data
from modules.selectors import BS4_SELECTORS


class RequestsParser:
    """Fetch and parse HTML pages using Requests and BeautifulSoup."""

    def __init__(self, url):
        """Store the target page URL."""
        self.url = url

    def get_page(self):
        """Send an HTTP request and return the server response."""
        response = requests.get(
            self.url,
            headers={'User-Agent': 'Mozilla/5.0'},
            timeout=10,
        )
        response.raise_for_status()
        return response

    def parse_page(self, response):
        """Extract product information from the HTML page."""
        soup = BeautifulSoup(response.text, 'html.parser')
        product_data = create_product_data()

        # Extract the product title.
        title_element = soup.select_one(BS4_SELECTORS['title'])

        if title_element is not None:
            product_data['title'] = title_element.get_text(strip=True)

        return product_data

if __name__ == '__main__':
    parser = RequestsParser('https://example.com')
    response = parser.get_page()
    product_data = parser.parse_page(response)

    pprint(product_data)
