#!/usr/bin/env bash

# TG Mod - Установка и запуск всего

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
NC='\033[0m' # No Color

# Проверка Python
echo -e "${BLUE}[1/5]${NC} Проверка Python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 не найден!${NC}"
    echo "Установи Python 3.9+ с https://python.org"
    exit 1
fi
echo -e "${GREEN}✓ Python найден:${NC} $(python3 --version)"

# Проверка Node.js
echo ""
echo -e "${BLUE}[2/5]${NC} Проверка Node.js..."
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js не найден!${NC}"
    echo "Установи Node.js с https://nodejs.org"
    exit 1
fi
echo -e "${GREEN}✓ Node.js найден:${NC} $(node --version)"
echo -e "${GREEN}✓ npm найден:${NC} $(npm --version)"

# Установка Python зависимостей
echo ""
echo -e "${BLUE}[3/5]${NC} Установка Python зависимостей..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Виртуальное окружение создано${NC}"
fi

source venv/bin/activate 2>/dev/null || . venv/Scripts/activate

if [ -f "requirements.txt" ]; then
    pip install -q -r requirements.txt
    echo -e "${GREEN}✓ Python пакеты установлены${NC}"
else
    echo -e "${YELLOW}⚠ requirements.txt не найден${NC}"
fi

# Установка Web UI зависимостей
echo ""
echo -e "${BLUE}[4/5]${NC} Установка Web UI зависимостей..."
cd ui/web

if [ ! -d "node_modules" ]; then
    npm install -q
    echo -e "${GREEN}✓ npm пакеты установлены${NC}"
else
    echo -e "${GREEN}✓ npm пакеты уже установлены${NC}"
fi

cd ../..

# Готово
echo ""
echo -e "${BLUE}[5/5]${NC} Финализация..."
echo ""
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Всё готово к запуску!${NC}"
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}📋 Запуск приложения:${NC}"
echo ""
echo -e "${YELLOW}Терминал 1 - Python API:${NC}"
echo -e "  ${BLUE}python core/main.py${NC}"
echo ""
echo -e "${YELLOW}Терминал 2 - Web UI:${NC}"
echo -e "  ${BLUE}cd ui/web && npm run dev${NC}"
echo ""
echo -e "${YELLOW}Откроется на:${NC}"
echo -e "  🌐 ${BLUE}http://localhost:5173${NC}"
echo ""
