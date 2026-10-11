# Brain.com.ua Product Parser

Python project for collecting product information from Brain.com.ua.

## Technologies

- Python
- Requests + BeautifulSoup
- Selenium
- Playwright
- Django
- PostgreSQL
- CSV

## Project Structure

- `parsers/` — product scraping implementations
- `product_selectors/` — CSS and XPath selectors
- `models/` — product data structures
- `services/` — product processing and persistence logic
- `exporters/` — CSV export
- `backend/` — Django application
- `tests/` — automated tests

## Installation

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium
```

## Status

Work in progress.