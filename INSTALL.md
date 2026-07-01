# TG Mod - Быстрая установка

## Windows

```bash
# Просто запусти файл
install.bat
```

Или в PowerShell/CMD:

```bash
cd Mod-tg
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cd ui/web
npm install
```

## macOS / Linux

```bash
# Сделай файл исполняемым и запусти
chmod +x install.sh
./install.sh
```

Или вручную:

```bash
cd Mod-tg
python3 -m venv venv
source venv/bin/activate  # или: . venv/Scripts/activate
pip install -r requirements.txt
cd ui/web
npm install
```

---

## ✅ После установки

**Терминал 1 - Python API:**

```bash
python core/main.py
```

**Терминал 2 - Web UI:**

```bash
cd ui/web
npm run dev
```

Откройся на **http://localhost:5173** 🚀
