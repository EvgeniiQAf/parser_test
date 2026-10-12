# Шпаргалка: Команди запуску проєкту Brain.ua Parser

Усі команди запускаються з кореневої директорії проєкту з активованим віртуальним середовищем (`source .venv/bin/activate`) або через префікс `.venv/bin/python`.

---

## 1. Запуск парсерів через CLI (`main.py`)

### ⚡ Швидкий запуск (Requests + curl_cffi)
> Працює за ~1-2 секунди, обходить Cloudflare через impersonate Chrome.
```bash
.venv/bin/python main.py --parser requests
```

### 🌐 Запуск Selenium (undetected_chromedriver)
> Запускає браузер Google Chrome, здійснює пошук, переходить на товар і розкриває характеристики.
```bash
.venv/bin/python main.py --parser selenium
```

### 🎭 Запуск Playwright (Chromium Stealth)
> Запускає Playwright Chromium із постійним збереженням сесії та захистом від блокувань.
```bash
.venv/bin/python main.py --parser playwright
```

---

## 2. Збереження зібраних даних

### 📄 Збереження в CSV файл
Дані записуються в `output/products.csv` (кирилиця зберігається коректно для Excel):
```bash
.venv/bin/python main.py --parser requests --csv
```

Задати власний шлях до файлу CSV:
```bash
.venv/bin/python main.py --parser requests --csv --csv-path output/my_phones.csv
```

### 🗄 Збереження в базу даних (Django ORM)
Створює або оновлює товар у базі даних (без дублювання завдяки `product_code`):
```bash
.venv/bin/python main.py --parser requests --db
```

### 🚀 Повний цикл (Екран + CSV + База даних одночасно)
```bash
.venv/bin/python main.py --parser requests --csv --db
```

---

## 3. Веб-інтерфейс Django (Адмін-панель)

### Запуск веб-сервера
```bash
.venv/bin/python backend/manage.py runserver
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
