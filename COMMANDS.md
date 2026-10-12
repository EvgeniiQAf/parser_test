# Шпаргалка: Команди запуску проєкту Brain.ua Parser

Усі команди запускаються з кореневої директорії проєкту з активованим віртуальним середовищем (`source .venv/bin/activate`) або через префікс `.venv/bin/python`.

---

## 1. Логіка прапорців збереження (CLI Flags)

| Команда / Прапорець | Що робить | Результат |
| :--- | :--- | :--- |
| **Без прапорців** | Тільки вивід на екран | Дані відображаються у таблиці в терміналі, **файли та БД не змінюються**. |
| `--csv` | Збереження у файл | Дописує товар у файл `output/products.csv`. |
| `--db` | Збереження в базу даних | Додає або оновлює товар у SQLite через Django ORM. |
| `--csv --db` | **Повне збереження** | Одночасно: вивід у термінал + запис у CSV + запис у базу даних. |

> [!NOTE]
> За замовчуванням парсер працює **без збереження** (тільки перегляд). Щоб зафіксувати результат, обов'язково вказуйте `--csv`, `--db` або обидва разом.

---

## 2. Запуск парсерів: без прапорців та з прапорцями

### 🌐 Selenium (`undetected_chromedriver`)
Шукає товар на Brain.ua за запитом `SELENIUM_SEARCH_TEXT` з `config.py`.

* **Тільки екран (без прапорців):**
  ```bash
  .venv/bin/python main.py --parser selenium
  ```
* **Зі збереженням у CSV:**
  ```bash
  .venv/bin/python main.py --parser selenium --csv
  ```
* **Зі збереженням у базу даних:**
  ```bash
  .venv/bin/python main.py --parser selenium --db
  ```
* **Повний запуск (екран + CSV + база даних):**
  ```bash
  .venv/bin/python main.py --parser selenium --csv --db
  ```

---

### 🎭 Playwright (Chromium Stealth)
Шукає товар на Brain.ua за запитом `PLAYWRIGHT_SEARCH_TEXT` з `config.py`.

* **Тільки екран (без прапорців):**
  ```bash
  .venv/bin/python main.py --parser playwright
  ```
* **Зі збереженням у CSV:**
  ```bash
  .venv/bin/python main.py --parser playwright --csv
  ```
* **Зі збереженням у базу даних:**
  ```bash
  .venv/bin/python main.py --parser playwright --db
  ```
* **Повний запуск (екран + CSV + база даних):**
  ```bash
  .venv/bin/python main.py --parser playwright --csv --db
  ```

---

### ⚡ Requests + curl_cffi (Прямий URL)
Миттєвий парсинг за прямою адресою товару `PRODUCT_URL` з `config.py`.

* **Тільки екран (без прапорців):**
  ```bash
  .venv/bin/python main.py --parser requests
  ```
* **Зі збереженням у CSV:**
  ```bash
  .venv/bin/python main.py --parser requests --csv
  ```
* **Зі збереженням у базу даних:**
  ```bash
  .venv/bin/python main.py --parser requests --db
  ```
* **Повний запуск (екран + CSV + база даних):**
  ```bash
  .venv/bin/python main.py --parser requests --csv --db
  ```

* **З власним шляхом до CSV файлу:**
  ```bash
  .venv/bin/python main.py --parser requests --csv --csv-path output/custom_file.csv
  ```


---

## 3. Веб-інтерфейс Django (Адмін-панель)

### Запуск веб-сервера
```bash
.venv/bin/python web_service/manage.py runserver
```

Після запуску відкрийте браузер за адресою:
👉 **http://127.0.0.1:8000/** (автоматично перенаправить на `/admin/`)

**Дані для входу в адмінку:**
- **Логін:** `admin`
- **Пароль:** `admin12345`

Тут можна переглядати, фільтрувати та шукати всі товари, збережені в базі даних.

---

## 4. Контроль якості, тести та лінтинг

### Запуск модульних тестів (Pytest)
Запускає всі 10 автоматичних тестів:
```bash
.venv/bin/python -m pytest tests/ -v
```

### Перевірка лінтером Ruff
```bash
.venv/bin/python -m ruff check .
```

### Перевірка лінтером Flake8 (PEP8, довжина рядків <= 88)
```bash
.venv/bin/python -m flake8 .
```

---

## 5. Робота з Git

### Перевірка статусу змін:
```bash
git status
```

### Створення фінального коміту:
```bash
git add .
git commit -m "Complete Brain.ua parser test task: OOP, SOLID, CSV export, Django ORM"
```

### Відправка на GitHub:
```bash
git push origin main
```
