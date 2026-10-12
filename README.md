# Brain.ua Product Parser

Проєкт для парсингу товарів з інтернет-магазину Brain.ua на позицію Junior Python Developer. Реалізовано з дотриманням принципів **ООП** та **SOLID**, із підтримкою 3 рушіїв скрапінгу, експорту в CSV та збереженням у реляційну базу даних через Django ORM.

---

## 🛠 Технологічний стек

- **Мова:** Python 3.12+
- **Парсинг:**
  - `curl_cffi` + `BeautifulSoup4` (швидкий HTTP-парсер із bypass Cloudflare)
  - `Selenium` + `undetected_chromedriver` (пошук та навігація в реальному Chrome)
  - `Playwright` + `playwright_stealth` (браузерний парсинг із постійним профілем сесії)
- **Бекенд та збереження даних:**
  - `Django` ORM
  - `PostgreSQL` / `SQLite` (автоматичний fallback для зручності локального запуску)
  - `CSV` (кодування `utf-8-sig` для коректного відображення кирилиці в Excel)
- **Консольний інтерфейс:** `Rich` (стилізовані таблиці та кольоровий вивід)
- **Контроль якості коду та тести:** `pytest`, `flake8` (max-line-length=88), `ruff`

---

## 📁 Структура проєкту

```text
├── backend/                  # Django проєкт та додатки
│   ├── config/              # Налаштування Django (settings, urls, wsgi)
│   ├── products/            # Додаток продуктів (models, admin, migrations)
│   └── manage.py            # Утиліта керування Django
├── exporters/               # Модулі експорту даних (CSV)
├── models/                  # Датаклас Product та фабричні методи
├── modules/                 # Ініціалізація Django оточення (load_django)
├── parsers/                 # Реалізація парсерів (BaseParser, Requests, Selenium, Playwright)
├── product_selectors/       # CSS та стійкі XPath селектори
├── services/                # Сервіси представлення (Rich) та збереження (DB)
├── tests/                   # Набір модульних тестів (pytest)
├── main.py                  # Єдина CLI точка входу
├── requirements.txt         # Залежності проєкту
└── README.md
```

---

## 🚀 Встановлення та налаштування

### 1. Клонування та створення віртуального середовища
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Встановлення залежностей
```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. Налаштування бази даних та міграції
За замовчуванням проєкт працює на **SQLite** (`db.sqlite3`). 

Для підключення до **PostgreSQL** створіть файл `.env` на основі `.env.example`:
```env
DB_NAME=brain_parser
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

Застосуйте міграції:
```bash
python backend/manage.py migrate
```

---

## 💻 Використання (CLI)

Запуск здійснюється через єдину точку входу `main.py` з гнучкими аргументами:

```bash
# Довідка за всіма аргументами
python main.py --help
```

### Приклади запуску:

1. **Швидкий запуск через Requests (curl_cffi):**
   ```bash
   python main.py --parser requests
   ```

2. **Запуск через Selenium (відкриття Chrome та навігація):**
   ```bash
   python main.py --parser selenium
   ```

3. **Запуск через Playwright:**
   ```bash
   python main.py --parser playwright
   ```

4. **Парсинг з експортом у CSV:**
   ```bash
   python main.py --parser requests --csv
   # Файл буде збережено в: output/products.csv
   ```

5. **Парсинг зі збереженням у базу даних (Django ORM):**
   ```bash
   python main.py --parser requests --db
   ```

6. **Повний цикл (вивід у термінал + CSV + База даних):**
   ```bash
   python main.py --parser requests --csv --db
   ```

---

## 🛡 Адміністративна панель Django

Для перегляду збережених товарів у веб-інтерфейсі створіть суперкористувача та запустіть сервер:
```bash
python backend/manage.py createsuperuser
python backend/manage.py runserver
```
Панель керування доступна за адресою: `http://127.0.0.1:8000/admin/`

---

## 🧪 Тестування та перевірка лінтерами

### Запуск модульних тестів (pytest):
```bash
pytest tests/ -v
```

### Перевірка якості коду (Flake8 та Ruff):
```bash
ruff check .
flake8 .
```