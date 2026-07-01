@echo off
REM TG Mod - Установка и запуск всего (Windows)

color 0A
cls

echo.
echo ════════════════════════════════════════
echo   TG Mod - Полная установка
echo   Python Core + Web UI
echo ════════════════════════════════════════
echo.

REM Проверка Python
echo [1/5] Проверка Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Ошибка: Python не найден!
    echo Установи Python 3.9+ с https://python.org
    pause
    exit /b 1
)
echo ✓ Python найден: 
for /f "tokens=*" %%i in ('python --version') do echo   %%i

REM Проверка Node.js
echo.
echo [2/5] Проверка Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Ошибка: Node.js не найден!
    echo Установи Node.js с https://nodejs.org
    pause
    exit /b 1
)
echo ✓ Node.js найден: 
for /f "tokens=*" %%i in ('node --version') do echo   %%i
echo ✓ npm найден:
for /f "tokens=*" %%i in ('npm --version') do echo   %%i

REM Установка Python зависимостей
echo.
echo [3/5] Установка Python зависимостей...
if not exist "venv" (
    python -m venv venv
    echo ✓ Виртуальное окружение создано
)

call venv\Scripts\activate.bat

if exist "requirements.txt" (
    pip install -q -r requirements.txt
    echo ✓ Python пакеты установлены
) else (
    echo ⚠ requirements.txt не найден
)

REM Установка Web UI зависимостей
echo.
echo [4/5] Установка Web UI зависимостей...
cd ui\web

if not exist "node_modules" (
    call npm install -q
    echo ✓ npm пакеты установлены
) else (
    echo ✓ npm пакеты уже установлены
)

cd ..\.

REM Готово
echo.
echo [5/5] Финализация...
echo.
echo ═══════════════════════════════════════
echo ✓ Всё готово к запуску!
echo ═══════════════════════════════════════
echo.
echo Запуск приложения:
echo.
echo Терминал 1 - Python API:
echo   python core\main.py
echo.
echo Терминал 2 - Web UI:
echo   cd ui\web && npm run dev
echo.
echo Откроется на:
echo   http://localhost:5173
echo.
pause
