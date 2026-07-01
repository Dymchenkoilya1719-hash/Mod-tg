# TG Mod — Модифицированный клиент Telegram

**Пользовательский MTProto-клиент на Python с поддержкой мобильного (Flutter) и десктопного интерфейса.**

## 🎯 Описание

TG Mod — это полнофункциональный клиент Telegram, разработанный в русском стиле с фокусом на удобство, безопасность и локальное кеширование. Проект использует:

- **Telethon** — Python MTProto библиотека
- **FastAPI** — локальный HTTP API
- **Flutter** — мобильный UI (кроссплатформенный)
- **SQLite** — метаданные и история
- **AES-256** — шифрование сессий

## ✨ Особенности

✅ **Аутентификация:** Вход по номеру → код → 2FA (если нужна)  
✅ **Синхронизация:** Импорт всех диалогов, чатов, каналов, супергрупп  
✅ **Сообщения:** Текст, фото, видео, стикеры, аудио, документы  
✅ **Функции:** Редактирование, удаление, пересылка, поиск  
✅ **Специальные чаты:** Поддержка (https://t.me/Rick666u) и ИИ (https://t.me/chat_gpt_unlim_bot)  
✅ **Безопасность:** Локальное шифрование, кеш, оффлайн-режим  
✅ **Дизайн:** Тёмно-зелёный (#1f6f3b), кремовый (#f7efe2), PT Sans/Rubik  
✅ **Темы:** Светлая/тёмная, PIN/biometric  

## 🚀 Быстрый старт

### 1. Требования

```bash
Python 3.9+
Node.js (для web UI)
Flutter SDK (для мобильного)
```

### 2. Установка

```bash
git clone https://github.com/Dymchenkoilya1719-hash/Mod-tg.git
cd Mod-tg

# Python зависимости
pip install -r requirements.txt

# Flutter зависимости (опционально)
cd ui/flutter_app
flutter pub get
```

### 3. Получение API ключей

1. Перейди на https://my.telegram.org
2. Залогинься аккаунтом Telegram
3. Перейди в **API development tools**
4. Создай приложение и получи `api_id` и `api_hash`
5. Скопируй их в `.env` файл

```bash
echo "API_ID=YOUR_API_ID" > .env
echo "API_HASH=YOUR_API_HASH" >> .env
echo "SESSION_PASSWORD=your_password" >> .env
```

### 4. Запуск

```bash
# Запуск Python-ядра (FastAPI)
python core/main.py

# Ядро запустится на http://localhost:8000
# Swagger API: http://localhost:8000/docs

# В отдельном терминале: Flutter UI
cd ui/flutter_app
flutter run
```

## 📁 Структура проекта

```
Mod-tg/
├── core/                          # Python-ядро (Telethon)
│   ├── main.py                    # Главный файл, FastAPI приложение
│   ├── telethon_client.py         # Telethon клиент логика
│   ├── auth.py                    # Аутентификация
│   ├── crypto.py                  # Шифрование/дешифрование сессий (AES-256)
│   ├── database.py                # SQLite логика
│   ├── cache.py                   # Кеш медиа
│   ├── sync.py                    # Синхронизация диалогов
│   └── models.py                  # Pydantic models
│
├── ui/
│   ├── flutter_app/               # Flutter мобильное приложение
│   │   ├── lib/
│   │   │   ├── main.dart
│   │   │   ├── screens/
│   │   │   │   ├── login_screen.dart
│   │   │   │   ├── chats_screen.dart
│   │   │   │   ├── chat_view_screen.dart
│   │   │   │   └── settings_screen.dart
│   │   │   ├── widgets/
│   │   │   ├── theme/
│   │   │   └── services/
│   │   └── pubspec.yaml
│
├── tests/                         # Unit tests
│   ├── test_auth.py
│   ├── test_crypto.py
│   └── conftest.py
│
├── docs/                          # Документация
│   ├── API.md                     # OpenAPI spec
│   ├── SETUP.md                   # Пошаговая установка
│   ├── ARCHITECTURE.md            # Архитектура
│   └── SECURITY.md                # Безопасность
│
├── .env.example                   # Пример переменных окружения
├── requirements.txt               # Python зависимости
└── LICENSE
```

## 🎨 Дизайн и цвета

| Компонент | Hex | RGB |
|-----------|-----|-----|
| Первичный | #1f6f3b | rgb(31, 111, 59) |
| Фон | #f7efe2 | rgb(247, 239, 226) |
| Акцент | #8b5a3c | rgb(139, 90, 60) |
| Тёмный | #1a1a1a | rgb(26, 26, 26) |
| Светлый | #ffffff | rgb(255, 255, 255) |

**Шрифты:** PT Sans, Rubik

## 📡 API Endpoints

### Аутентификация

```
POST   /api/auth/request_code       → запрос кода по номеру
POST   /api/auth/sign_in            → вход с кодом и паролем 2FA
POST   /api/auth/logout             → выход
GET    /api/auth/me                 → текущий пользователь
```

### Диалоги

```
GET    /api/dialogs                 → список всех диалогов
GET    /api/dialogs/{dialog_id}     → информация о диалоге
GET    /api/dialogs/{dialog_id}/messages  → сообщения
```

### Сообщения

```
POST   /api/messages/send           → отправить сообщение
PUT    /api/messages/{msg_id}       → отредактировать
DELETE /api/messages/{msg_id}       → удалить
POST   /api/messages/{msg_id}/forward  → переслать
```

## 🔒 Безопасность

⚠️ **Важно:**

1. Сессии шифруются локально с помощью AES-256
2. Пароль для расшифровки НЕ передаётся на серверы
3. Кеш медиа хранится локально
4. Не нарушает Telegram ToS (используется официальный MTProto)

## 📱 Сборка для мобильных платформ

### Android

```bash
cd ui/flutter_app
flutter build apk --release
# APK будет в: build/app/outputs/flutter-apk/app-release.apk
```

### iOS

```bash
cd ui/flutter_app
flutter build ios --release
# IPA в: build/ios/iphoneos/
```

### Web

```bash
cd ui/flutter_app
flutter build web
# Выходные файлы в: build/web/
```

## 📚 Документация

- [SETUP.md](docs/SETUP.md) — Пошаговая установка
- [API.md](docs/API.md) — API документация
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) — Архитектура проекта
- [SECURITY.md](docs/SECURITY.md) — Безопасность

## 🤝 Контакты

- 🔗 Поддержка: https://t.me/Rick666u
- 🤖 ИИ чат: https://t.me/chat_gpt_unlim_bot

## ⚖️ Лицензия

MIT License. Используй в образовательных целях.

**Дисклеймер:** Это неофициальный клиент Telegram. Убедись, что соблюдаешь [Telegram ToS](https://core.telegram.org/api/obtaining_api_id).

---

**Разработано с ❤️ для русскоязычного сообщества.**
