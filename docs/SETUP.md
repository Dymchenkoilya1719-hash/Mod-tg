# 📖 Пошаговая инструкция по установке TG Mod

## ✅ Шаг 1: Получение API ключей

### Для получения `api_id` и `api_hash`:

1. Перейди на https://my.telegram.org
2. Залогинься с помощью номера телефона
3. Введи код из Telegram приложения
4. Выбери **"API development tools"**
5. На странице **"API development tools"**:
   - **App title**: "TG Mod" (любое н��звание)
   - **Short name**: "tg_mod" (латиница, без пробелов)
   - **Platform**: "Desktop" или "Other"
   - **Description**: "Custom Telegram client"
6. Нажми **"Create application"**
7. Скопируй:
   - **api_id** (число)
   - **api_hash** (строка символов)

⚠️ **Важно:** Никогда не делись этими ключами публично!

## ✅ Шаг 2: Установка зависимостей

### Требования системы:

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3.9-dev python3-pip git

# macOS (через Homebrew)
brew install python@3.9 git

# Windows
# Скачай Python 3.9+ с python.org
# Убедись, что выбрал "Add Python to PATH" при установке
```

### Python пакеты:

```bash
cd Mod-tg
pip install -r requirements.txt
```

## ✅ Шаг 3: Конфигурация

### Создай `.env` файл:

```bash
cp .env.example .env
```

### Отредактируй `.env`:

```ini
# Вставь полученные ключи
API_ID=YOUR_API_ID_HERE
API_HASH=your_api_hash_here_1234567890abcdef1234567890abcdef

# Пароль для шифрования сессии (придумай сильный пароль)
SESSION_PASSWORD=MySecurePassword123!@#

# Настройки API сервера
API_HOST=0.0.0.0
API_PORT=8000

# Пути данных
DB_PATH=data/tg_mod.db
CACHE_DIR=data/cache
CACHE_MAX_SIZE_MB=500

# Debug режим (для разработки)
DEBUG=true
```

## ✅ Шаг 4: Запуск API сервера

```bash
# Из корневой папки проекта
python core/main.py
```

Если всё ОК, ты увидишь:

```
╔════════════════════════════════════════════════════╗
║           TG Mod - Telegram Client API            ║
║                  v1.0.0                           ║
╚════════════════════════════════════════════════════╝

[*] Starting API server on http://0.0.0.0:8000
[*] Swagger UI: http://localhost:8000/docs
[*] Database: data/tg_mod.db
[*] Cache: data/cache

INFO:     Uvicorn running on http://0.0.0.0:8000
```

## ✅ Шаг 5: Тестирование API

### Вариант 1: Через Swagger UI

1. Открой http://localhost:8000/docs в браузере
2. Нажми на кнопку **"Try it out"** рядом с `/api/auth/request_code`
3. Введи свой номер телефона в формате: `+7XXXXXXXXXX` (для России)
4. Нажми **"Execute"**

### Вариант 2: Через curl

```bash
# Запрос кода
curl -X POST "http://localhost:8000/api/auth/request_code" \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+7XXXXXXXXXX"}'

# Ответ (пример):
# {"success": true, "phone_code_hash": "abc123..."}
```

### Вариант 3: Через Python

```python
import requests

API_URL = "http://localhost:8000"

# Запрос кода
response = requests.post(
    f"{API_URL}/api/auth/request_code",
    json={"phone_number": "+7XXXXXXXXXX"}
)
print(response.json())
```

## ✅ Шаг 6: Авторизация

После запроса кода ты получишь SMS/Telegram с 5-значным кодом.

```bash
# Вход с кодом (и паролем 2FA если требуется)
curl -X POST "http://localhost:8000/api/auth/sign_in" \
  -H "Content-Type: application/json" \
  -d '{"code": "12345", "password": null}'

# Или с 2FA
curl -X POST "http://localhost:8000/api/auth/sign_in" \
  -H "Content-Type: application/json" \
  -d '{"code": "12345", "password": "your_2fa_password"}'
```

## ✅ Шаг 7: Проверка авторизации

```bash
# Проверь текущего пользователя
curl -X GET "http://localhost:8000/api/auth/me"

# Ответ:
# {
#   "id": 123456789,
#   "first_name": "Иван",
#   "last_name": "Петров",
#   "phone": "+7XXXXXXXXXX",
#   "username": "ivan_petrov"
# }
```

## ✅ Шаг 8: Синхронизация диалогов

```bash
# Запустить синхронизацию
curl -X POST "http://localhost:8000/api/sync"

# Получить список диалогов
curl -X GET "http://localhost:8000/api/dialogs"
```

## 🆘 Решение проблем

### Ошибка: "API_ID not found in .env"

✅ **Решение:** Создай `.env` файл и добавь `API_ID` и `API_HASH`

```bash
cp .env.example .env
# Отредактируй .env с помощью текстового редактора
```

### Ошибка: "Invalid API ID"

✅ **Решение:** Проверь, что `API_ID` — это число, а не строка

### Ошибка: "Connection refused"

✅ **Решение:** Убедись, что сервер запущен:

```bash
python core/main.py
```

### Ошибка при SMS коде: "The code is invalid"

✅ **Решение:** 
- Убедись, что вводишь правильный код
- Код действует только 5 минут
- Если истёк, запроси новый

### Ошибка 2FA: "password_hash_invalid"

✅ **Решение:** Если у тебя включена двухфакторная аутентификация:
1. Проверь пароль (учитывается регистр)
2. Убедись, что его вводишь в параметре `password`

---

**Готово!** Твой TG Mod API полностью настроен и работает. 🚀
