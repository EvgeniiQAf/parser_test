# Brain.ua Product Scraper

A Python project for scraping product information from the Brain.ua online store, developed as a technical assignment for a **Junior Python Developer** position.

The project follows **Object-Oriented Programming (OOP)** and **SOLID** principles, organized with a clean domain-driven architecture, supporting three scraping engines, CSV export, and product data storage in a relational database using Django ORM.

---

## 🛠 Tech Stack

- **Language:** Python 3.12+
- **Web Scraping:**
  - `curl_cffi` + `BeautifulSoup4` — HTTP-based scraping with browser impersonation to bypass Cloudflare protection.
  - `Selenium` + `undetected_chromedriver` — browser automation, product search, and navigation using Chrome.
  - `Playwright` + `playwright_stealth` — browser-based scraping with a persistent browser session.
- **Web Service and Data Storage:**
  - `Django` ORM + Admin Dashboard
  - `PostgreSQL` / `SQLite` — automatic SQLite fallback for convenient local development.
  - `CSV` — UTF-8 with BOM (`utf-8-sig`) for proper Cyrillic character display in Excel.
- **Console Output:** `Rich` — formatted tables and colored terminal output.
- **Code Quality and Testing:** `pytest`, `flake8` (max-line-length=88), `ruff`.

---

## 📁 Project Architecture

The codebase is organized into cohesive packages separating data collection, web persistence, and tests:

```text
python_parser_test/
├── 📂 scraper/                   # Data collection package (everything scraping)
│   ├── 📂 engines/               # Scraping engines
│   │   ├── base_scraper.py       # BaseScraper abstract interface
│   │   ├── requests_scraper.py   # Fast HTTP scraper (curl_cffi)
│   │   ├── selenium_scraper.py   # Chrome scraper (Selenium)
│   │   └── playwright_scraper.py # Chromium scraper (Playwright)
│   ├── models.py                 # ScrapedProduct (DTO for collected data)
│   ├── selectors.py              # Robust XPath and CSS selectors
│   ├── utils.py                  # Text cleaning, price & number parsing helpers
│   ├── exporters.py              # CSV exporter (CsvExporter)
│   └── display.py                # Rich terminal presentation service
│
├── 📂 web_service/               # Django web service and persistence layer
│   ├── 📂 config/                # Django settings, URLs, and WSGI configuration
│   ├── 📂 products/              # Products app (ProductModel, admin, migrations)
│   ├── db_service.py             # Database service: ScrapedProduct -> ProductModel
│   └── manage.py                 # Django management CLI utility
│
├── 📂 tests/                     # Test suite
│   └── test_scrapers.py          # 10 automated unit tests (pytest)
│
├── 📄 main.py                    # Main CLI entry point (orchestrator)
├── 📄 config.py                  # User search queries and URL configuration
├── 📄 requirements.txt          # Project dependencies
└── 📄 COMMANDS.md                # Detailed quick-reference guide for all commands
```

---

## 🚀 Installation and Setup

### 1. Clone the Repository and Create a Virtual Environment

```bash
git clone https://github.com/EvgeniiQAf/parser_test.git
cd parser_test

python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. Database Configuration and Migrations

By default, the project uses **SQLite** (`db.sqlite3`).

To use **PostgreSQL**, create a `.env` file based on `.env.example`:

```env
DB_NAME=brain_parser
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

Apply database migrations:

```bash
python web_service/manage.py migrate
```

---

## 💻 Usage (CLI)

The application uses a single entry point, `main.py`, with command-line arguments:

```bash
# View all available CLI options
python main.py --help
```

### Usage Examples:

**1. Run the Requests / curl_cffi scraper:**
```bash
python main.py --scraper requests
```

**2. Run the Selenium scraper:**
```bash
python main.py --scraper selenium
```

**3. Run the Playwright scraper:**
```bash
python main.py --scraper playwright
```

**4. Scrape and export to CSV:**
```bash
python main.py --scraper requests --csv
# File will be saved to: output/products.csv
```

**5. Scrape and save to database (Django ORM):**
```bash
python main.py --scraper requests --db
```

**6. Complete workflow (Terminal output + CSV + Database):**
```bash
python main.py --scraper requests --csv --db
```

*(Note: `--parser` flag is fully supported as a backward-compatible alias for `--scraper`)*.

---

## 🛡 Django Admin Panel

To view and manage stored product records in the browser:

```bash
python web_service/manage.py createsuperuser
python web_service/manage.py runserver
```

Open in browser: **http://127.0.0.1:8000/** (automatically redirects to `/admin/`).
- **Default Login:** `admin`
- **Default Password:** `admin12345`

---

## 🧪 Testing and Code Quality

### Run Unit Tests (pytest)
```bash
pytest -v
```

### Run Linters (Ruff and Flake8)
```bash
ruff check .
flake8 .
```

Flake8 is configured with a maximum line length of 88 characters.

---

## 📋 Technical Assignment

The project implements three independent product scrapers for [Brain.ua](https://brain.com.ua/):

- **Requests / curl_cffi:** Extracts product information directly from a specified product page.
- **Selenium:** Searches for a product, selects the matching result, and extracts all details.
- **Playwright:** Performs the same browser-based search and extraction independently using Playwright.

Each scraper collects product information, including the title, manufacturer, color, storage capacity, regular and promotional prices, image URLs, product code, review count, screen size, screen resolution, and technical specifications.
