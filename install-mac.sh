#!/usr/bin/env zsh
# TG Mod - Установка и запуск всего (macOS)

echo ""
echo "╔════════════════════════════════════════╗"
echo "║  🚀 TG Mod - Полная установка         ║"
echo "║     Python Core + Web UI               ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Цвета
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Проверка Python
echo "${BLUE}[1/5]${NC} Проверка Python..."
if ! command -v python3 &> /dev/null; then
    echo "${RED}❌ Python3 не найден!${NC}"
    echo "Установи: brew install python@3.11"
    exit 1
fi
echo "${GREEN}✓ Python найден:${NC} $(python3 --version)"

# Проверка Node.js
echo ""
echo "${BLUE}[2/5]${NC} Проверка Node.js..."
if ! command -v node &> /dev/null; then
    echo "${RED}❌ Node.js не найден!${NC}"
    echo "Установи: brew install node"
    exit 1
fi
echo "${GREEN}✓ Node.js найден:${NC} $(node --version)"
echo "${GREEN}✓ npm найден:${NC} $(npm --version)"

# Установка Python зависимостей
echo ""
echo "${BLUE}[3/5]${NC} Установка Python зависимостей..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "${GREEN}✓ Виртуальное окружение создано${NC}"
fi

source venv/bin/activate

if [ -f "requirements.txt" ]; then
    pip install -q -r requirements.txt
    echo "${GREEN}✓ Python пакеты установлены${NC}"
else
    echo "${YELLOW}⚠ requirements.txt не найден${NC}"
fi

# Установка Web UI зависимостей
echo ""
echo "${BLUE}[4/5]${NC} Установка Web UI зависимостей..."
cd ui/web

if [ ! -d "node_modules" ]; then
    npm install -q
    echo "${GREEN}✓ npm пакеты установлены${NC}"
else
    echo "${GREEN}✓ npm пакеты уже установлены${NC}"
fi

cd ../..

# Готово
echo ""
echo "${BLUE}[5/5]${NC} Финализация..."
echo ""
echo "${GREEN}═══════════════════════════════════════${NC}"
echo "${GREEN}✓ Всё готово к запуску!${NC}"
echo "${GREEN}═══════════════════════════════════════${NC}"
echo ""
echo "${YELLOW}📋 Запуск приложения:${NC}"
echo ""
echo "${YELLOW}Терминал 1 - Python API:${NC}"
echo "  ${BLUE}python core/main.py${NC}"
echo ""
echo "${YELLOW}Терминал 2 - Web UI:${NC}"
echo "  ${BLUE}cd ui/web && npm run dev${NC}"
echo ""
echo "${YELLOW}Откроется на:${NC}"
echo "  🌐 ${BLUE}http://localhost:5173${NC}"
echo ""
