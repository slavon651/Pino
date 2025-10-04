# 🚀 Быстрый старт / Quick Setup Guide

## 🇷🇺 Русская версия

### Минимальные требования
- Python 3.8 или выше
- pip (менеджер пакетов Python)

### Быстрый запуск (Linux/Mac)

1. **Клонируйте или скачайте проект**

2. **Запустите скрипт установки:**
```bash
chmod +x run.sh
./run.sh
```

3. **Откройте браузер:**
```
http://localhost:5000
```

Готово! 🎉

### Ручная установка

1. **Создайте виртуальное окружение:**
```bash
python3 -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
```

2. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

3. **Запустите приложение:**
```bash
python3 app.py
```

4. **Откройте в браузере:**
```
http://localhost:5000
```

### Установка через Docker

Если у вас установлен Docker:

```bash
# Сборка и запуск
docker-compose up -d

# Проверка статуса
docker-compose ps

# Остановка
docker-compose down
```

---

## 🇬🇧 English Version

### Requirements
- Python 3.8 or higher
- pip (Python package manager)

### Quick Start (Linux/Mac)

1. **Clone or download the project**

2. **Run the setup script:**
```bash
chmod +x run.sh
./run.sh
```

3. **Open your browser:**
```
http://localhost:5000
```

Done! 🎉

### Manual Installation

1. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python3 app.py
```

4. **Open in browser:**
```
http://localhost:5000
```

### Docker Installation

If you have Docker installed:

```bash
# Build and run
docker-compose up -d

# Check status
docker-compose ps

# Stop
docker-compose down
```

---

## 📦 Деплой в продакшен / Production Deployment

### С помощью Gunicorn (рекомендуется)

1. **Установите Gunicorn:**
```bash
pip install gunicorn
```

2. **Запустите:**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### С помощью Nginx (рекомендуется для продакшена)

1. **Настройте Nginx как reverse proxy:**

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

2. **Настройте SSL с Let's Encrypt:**
```bash
sudo certbot --nginx -d your-domain.com
```

### Heroku

1. **Создайте Procfile:**
```
web: gunicorn app:app
```

2. **Деплой:**
```bash
heroku create your-app-name
git push heroku main
```

### Railway.app

1. Загрузите проект на GitHub
2. Подключите репозиторий к Railway
3. Автоматический деплой готов!

---

## 🔧 Настройка SEO

### Google Search Console

1. Зайдите на https://search.google.com/search-console
2. Добавьте ваш сайт
3. Скопируйте код верификации
4. Вставьте в `templates/index.html` в строку:
```html
<meta name="google-site-verification" content="ВАШ_КОД">
```

### Яндекс Вебмастер

1. Зайдите на https://webmaster.yandex.ru
2. Добавьте ваш сайт
3. Скопируйте код верификации
4. Вставьте в `templates/index.html` в строку:
```html
<meta name="yandex-verification" content="ВАШ_КОД">
```

### Обновите домен

В файле `templates/index.html` замените `https://yourwebsite.com/` на ваш реальный домен во всех местах.

---

## 🐛 Решение проблем / Troubleshooting

### Порт 5000 занят
```bash
# Используйте другой порт
python3 app.py  # или измените в app.py на другой порт
```

### Ошибки установки зависимостей
```bash
# Обновите pip
pip install --upgrade pip

# Попробуйте установить заново
pip install -r requirements.txt --force-reinstall
```

### Видео не скачивается
- Проверьте, что URL правильный
- Убедитесь, что это публичное видео
- Попробуйте другое видео для теста

---

## 📞 Поддержка / Support

Если у вас возникли проблемы:
1. Проверьте этот файл SETUP.md
2. Посмотрите README.md
3. Создайте Issue в репозитории

---

## ⚡ Быстрые команды / Quick Commands

```bash
# Установка и запуск
./run.sh

# Только запуск (если уже установлено)
python3 app.py

# С виртуальным окружением
source venv/bin/activate && python3 app.py

# Docker
docker-compose up

# Проверка синтаксиса
python3 -m py_compile app.py

# Установка с пакетом gunicorn
pip install -r requirements.txt gunicorn

# Запуск в продакшен режиме
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

Удачи! 🚀✨
Good luck! 🚀✨
