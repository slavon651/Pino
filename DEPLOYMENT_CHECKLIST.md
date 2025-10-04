# 🚀 Чек-лист для деплоя / Deployment Checklist

## ✅ Перед деплоем / Before Deployment

### 1. Базовая настройка / Basic Setup
- [ ] Выбран домен (например: pinvidgrab.com)
- [ ] Приобретен хостинг или выбрана платформа (Heroku, Railway, VPS)
- [ ] Настроены DNS записи
- [ ] Получен SSL сертификат (Let's Encrypt или через хостинг)

### 2. Конфигурация приложения / App Configuration
- [ ] Обновлен домен в `templates/index.html`
  - Замените все `https://yourwebsite.com/` на ваш домен
- [ ] Проверены все пути к файлам
- [ ] Проверена работа приложения локально

### 3. SEO настройки / SEO Setup
- [ ] Зарегистрирован в Google Search Console
- [ ] Получен код верификации Google
- [ ] Добавлен код в `<meta name="google-site-verification">`
- [ ] Зарегистрирован в Яндекс Вебмастер
- [ ] Получен код верификации Яндекс
- [ ] Добавлен код в `<meta name="yandex-verification">`
- [ ] Обновлен файл `sitemap.xml` с правильным доменом
- [ ] Файл `robots.txt` настроен правильно

### 4. Безопасность / Security
- [ ] Настроен HTTPS (обязательно!)
- [ ] Добавлены security headers
- [ ] Настроен firewall
- [ ] Ограничен rate limiting (опционально)
- [ ] Проверены все зависимости на уязвимости

---

## 🔧 Деплой / Deployment

### Вариант 1: VPS (Ubuntu/Debian)

#### Шаг 1: Подготовка сервера
```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Python и необходимых пакетов
sudo apt install python3-pip python3-venv nginx -y

# Установка certbot для SSL
sudo apt install certbot python3-certbot-nginx -y
```

#### Шаг 2: Загрузка проекта
```bash
# Клонирование или загрузка
cd /var/www/
sudo git clone your-repo-url pinterest-downloader
cd pinterest-downloader

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt
pip install gunicorn
```

#### Шаг 3: Настройка Gunicorn
```bash
# Создание systemd service
sudo nano /etc/systemd/system/pinterest-downloader.service
```

Содержимое файла:
```ini
[Unit]
Description=Pinterest Video Downloader
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/pinterest-downloader
Environment="PATH=/var/www/pinterest-downloader/venv/bin"
ExecStart=/var/www/pinterest-downloader/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

```bash
# Запуск сервиса
sudo systemctl start pinterest-downloader
sudo systemctl enable pinterest-downloader
sudo systemctl status pinterest-downloader
```

#### Шаг 4: Настройка Nginx
```bash
sudo nano /etc/nginx/sites-available/pinterest-downloader
```

Содержимое файла:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/pinterest-downloader/static;
    }

    # robots.txt
    location /robots.txt {
        alias /var/www/pinterest-downloader/robots.txt;
    }

    # sitemap.xml
    location /sitemap.xml {
        alias /var/www/pinterest-downloader/sitemap.xml;
    }
}
```

```bash
# Активация конфигурации
sudo ln -s /etc/nginx/sites-available/pinterest-downloader /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Шаг 5: Настройка SSL
```bash
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

---

### Вариант 2: Docker

```bash
# Сборка образа
docker build -t pinterest-downloader .

# Запуск контейнера
docker run -d -p 5000:5000 --name pinterest-downloader pinterest-downloader

# Или через docker-compose
docker-compose up -d
```

---

### Вариант 3: Heroku

```bash
# Создание Procfile
echo "web: gunicorn app:app" > Procfile

# Инициализация git (если нужно)
git init
git add .
git commit -m "Initial commit"

# Создание приложения Heroku
heroku create your-app-name

# Деплой
git push heroku main

# Открытие приложения
heroku open
```

---

### Вариант 4: Railway.app

1. Загрузите проект на GitHub
2. Зайдите на railway.app
3. Нажмите "New Project"
4. Выберите "Deploy from GitHub"
5. Выберите ваш репозиторий
6. Railway автоматически развернет приложение
7. Настройте custom domain в настройках

---

## 📊 После деплоя / Post-Deployment

### 1. Проверка работоспособности
- [ ] Сайт открывается по основному домену
- [ ] HTTPS работает корректно
- [ ] Все стили и анимации загружаются
- [ ] Форма скачивания работает
- [ ] Тестовое видео скачивается успешно

### 2. Мониторинг
- [ ] Настроен мониторинг uptime (uptimerobot.com)
- [ ] Настроены alerts при падении сервера
- [ ] Логи доступны и проверяются

### 3. SEO финализация
- [ ] Отправлен sitemap.xml в Google Search Console
- [ ] Отправлен sitemap.xml в Яндекс Вебмастер
- [ ] Проверена индексация через site:yourdomain.com
- [ ] Настроен Google Analytics (опционально)
- [ ] Настроен Яндекс Метрика (опционально)

### 4. Оптимизация
- [ ] Включен gzip compression в nginx
- [ ] Настроен кеш статических файлов
- [ ] Проверена скорость через PageSpeed Insights
- [ ] Проверен Lighthouse score

---

## 🔍 Проверка SEO / SEO Check

### Google Search Console
```
1. Перейти: https://search.google.com/search-console
2. Добавить сайт
3. Верифицировать через meta tag
4. Отправить sitemap: https://yourdomain.com/sitemap.xml
5. Проверить покрытие индекса
```

### Яндекс Вебмастер
```
1. Перейти: https://webmaster.yandex.ru
2. Добавить сайт
3. Верифицировать через meta tag
4. Отправить sitemap
5. Проверить индексацию
```

### Проверка структурированных данных
```
1. Google Rich Results Test: https://search.google.com/test/rich-results
2. Вставить URL вашего сайта
3. Проверить, что JSON-LD корректно распознается
```

---

## 📈 Маркетинг / Marketing

### После запуска
- [ ] Пост в социальных сетях
- [ ] Регистрация в каталогах сайтов
- [ ] Статья в блоге о запуске
- [ ] Реддит пост (r/webdev, r/InternetIsBeautiful)
- [ ] Product Hunt запуск
- [ ] Обратные ссылки с других сайтов

---

## 🐛 Траблшутинг / Troubleshooting

### Сайт не открывается
```bash
# Проверка статуса сервиса
sudo systemctl status pinterest-downloader

# Проверка логов
sudo journalctl -u pinterest-downloader -f

# Проверка nginx
sudo nginx -t
sudo systemctl status nginx
```

### SSL не работает
```bash
# Перезапуск certbot
sudo certbot renew
sudo systemctl restart nginx
```

### Медленная работа
```bash
# Увеличение workers в gunicorn
# В systemd service изменить на -w 8
sudo systemctl restart pinterest-downloader
```

---

## ✅ Финальная проверка / Final Check

Перед объявлением о запуске:

1. ✅ Сайт работает на HTTPS
2. ✅ Все страницы загружаются быстро (< 3 сек)
3. ✅ Мобильная версия работает идеально
4. ✅ Скачивание видео работает
5. ✅ SEO теги на месте
6. ✅ Sitemap отправлен
7. ✅ Мониторинг настроен
8. ✅ Резервные копии настроены
9. ✅ Контактная информация добавлена
10. ✅ Privacy Policy и Terms добавлены (опционально)

---

## 🎉 Готово! / Ready!

Ваш сайт готов к запуску! 🚀

### Следующие шаги:
1. Начните продвижение
2. Следите за метриками
3. Собирайте feedback от пользователей
4. Постепенно улучшайте сервис
5. Радуйтесь успеху! 🎊

---

**Удачи с запуском!** 🌟
**Good luck with the launch!** 🌟
