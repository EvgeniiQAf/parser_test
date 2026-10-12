# Brain.ua Product Parser

A Python project for scraping product information from the Brain.ua online store, developed as a technical assignment for a **Junior Python Developer** position.

The project follows **Object-Oriented Programming (OOP)** and **SOLID** principles. It supports three scraping engines, CSV export, and product data storage in a relational database using Django ORM.

---

##  Tech Stack

- **Language:** Python 3.12+
- **Web Scraping:**
  - `curl_cffi` + `BeautifulSoup4` — HTTP-based scraping with browser impersonation to help handle Cloudflare protection.
  - `Selenium` + `undetected_chromedriver` — browser automation, product search, and navigation using Chrome.
  - `Playwright` + `playwright_stealth` — browser-based scraping with a persistent browser session.
- **Backend and Data Storage:**
  - `Django` ORM
  - `PostgreSQL` / `SQLite` — automatic SQLite fallback for easier local setup.
  - `CSV` — UTF-8 with BOM (`utf-8-sig`) for proper Cyrillic character display in Excel.
- **Console Output:** `Rich` — formatted tables and colored terminal output.
- **Code Quality and Testing:** `pytest`, `flake8` (max-line-length=88), `ruff`.

---

##  Project Structure

```text
├── backend/                  # Django project and applications
│   ├── config/               # Django settings, URLs, and WSGI configuration
│   ├── products/             # Product app (models, admin, migrations)
│   └── manage.py             # Django management utility
├── exporters/                # Data export modules (CSV)
├── models/                   # Product dataclass and factory methods
├── modules/                  # Django environment initialization (load_django)
├── parsers/                  # BaseParser, Requests, Selenium, and Playwright
├── product_selectors/        # CSS and XPath selectors
├── services/                 # Rich output and database persistence services
├── tests/                    # Unit tests (pytest)
├── main.py                   # Main CLI entry point
├── requirements.txt          # Project dependencies
└── README.md
```

---

##  Installation and Setup

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

To use **PostgreSQL**, create a `.env` file based on `.env.example` and configure the database connection:

```env
DB_NAME=brain_parser
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

Make sure the PostgreSQL server is running and the specified database exists.

Apply the database migrations:

```bash
python backend/manage.py migrate
```

**Note:** PostgreSQL is required by the technical assignment. SQLite is provided only as a convenient fallback for local development.

---

##  Usage (CLI)

The application uses a single entry point, `main.py`, with command-line arguments for selecting the parser and output options.

To view all available options:

```bash
python main.py --help
```

### Usage Examples

**1. Run the Requests / BeautifulSoup parser**

```bash
python main.py --parser requests
```

**2. Run the Selenium parser**

Opens Chrome, searches for the product, and extracts its details.

```bash
python main.py --parser selenium
```

**3. Run the Playwright parser**

```bash
python main.py --parser playwright
```

**4. Scrape product data and export it to CSV**

```bash
python main.py --parser requests --csv
```

The exported file will be saved to:

```text
output/products.csv
```

**5. Scrape product data and save it to the database using Django ORM**

```bash
python main.py --parser requests --db
```

**6. Run the complete workflow**

Scrape product information, display it in the terminal, export it to CSV, and save it to the database.

```bash
python main.py --parser requests --csv --db
```

---

##  Django Admin Panel

The Django admin interface allows you to view and manage stored product records.

Create a superuser:

```bash
python backend/manage.py createsuperuser
```

Start the development server:

```bash
python backend/manage.py runserver
```

Open the admin panel in your browser:

http://127.0.0.1:8000/admin/

Log in using your superuser credentials.

---

##  Testing and Code Quality

### Run Unit Tests (pytest)

```bash
pytest tests/ -v
```

### Run Ruff

```bash
ruff check .
```

### Run Flake8

```bash
flake8 .
```

Flake8 is configured with a maximum line length of 88 characters.

---

##  Technical Assignment

The project implements three independent product scrapers for [Brain.ua](https://brain.com.ua/):

- **Requests / BeautifulSoup:** Extracts product information directly from a specified product page.
- **Selenium:** Searches for a product, opens the first search result, and extracts its details.
- **Playwright:** Performs the same browser-based workflow independently using Playwright.

Each parser collects product information, including the title, manufacturer, color, storage capacity, regular and promotional prices, image URLs, product code, review count, screen size, screen resolution, and product specifications.

The collected data can be displayed in the terminal, saved to a database, and exported to CSV.
