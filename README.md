# PrometeyLabs Advertising Landing

🚀 **Production-Ready** лендінг для PrometeyLabs з розумним розрахунком вартості та ШІ рекомендаціями.

## 🎯 Основні можливості

- 🎨 **Сучасний UI/UX** з анімаціями та градієнтами
- 📝 **Інтелектуальний опитувальник** (6 кроків)
- 💰 **Розумний розрахунок ціни** ($209-499)
- 🤖 **ШІ персоналізація** результатів
- 📱 **Повна адаптивність** (iOS Safari + Android)
- ⚡ **Оптимізований код** без дублювання
- 🔐 **Production-ready** безпека

## 🛠 Технології

- **Backend**: Django 4.2.23
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Стилі**: Bootstrap 5 + Custom CSS with gradients
- **Безпека**: Whitenoise, CSRF protection, SSL ready
- **Deployment**: Heroku/Vercel ready

## 🚀 Швидкий старт

### 1. Клонування та налаштування
```bash
git clone https://github.com/your-username/prometeylabs-advertising.git
cd prometeylabs-advertising
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Налаштування бази даних
```bash
python manage.py migrate
python manage.py createsuperuser  # опціонально
```

### 3. Запуск локально
```bash
python manage.py runserver
```
Відкрийте: http://127.0.0.1:8000

## 🌐 Deployment

### Heroku
```bash
# Встановіть Heroku CLI
heroku create your-app-name
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False
git push heroku main
```

### Vercel
```bash
npm i -g vercel
vercel --prod
```

### Налаштування змінних середовища
Створіть `.env` файл:
```env
SECRET_KEY=your-secret-key-here-min-50-characters
DEBUG=False
DJANGO_ENV=production
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Опціонально
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

## 📊 Структура проекту

```
prometeylabs_advertising/
├── 🎛️ prometeylabs_landing/    # Django проект
│   ├── settings.py             # Налаштування (production-ready)
│   ├── environment.py          # Змінні середовища
│   ├── urls.py
│   └── wsgi.py
├── 🎨 landing/                 # Основний додаток
│   ├── 📊 models.py            # QuestionnaireResult модель
│   ├── 🧠 views.py             # Розумна логіка розрахунків
│   ├── 📝 forms.py             # Django форми
│   ├── 🔗 urls.py              # URL маршрутизація
│   ├── ⚙️ admin.py             # Адмін панель
│   ├── 📄 templates/landing/   # HTML шаблони
│   │   ├── index.html          # Лендінг з опитувальником
│   │   └── result.html         # Результати
│   └── 📁 static/landing/      # Статичні файли
│       ├── 🎨 css/style.css    # Оптимізовані стилі
│       ├── ⚡ js/script.js      # Очищений JavaScript
│       └── 🖼️ img/             # Зображення
├── 📦 requirements.txt         # Python залежності
├── 🚀 Procfile                 # Heroku конфігурація
├── 🐍 runtime.txt              # Python версія
├── 🙈 .gitignore               # Git виключення
├── 🌍 locale/                  # Локалізація (майбутнє)
└── 📖 README.md                # Ця документація
```

## 🧠 Логіка розрахунку ціни

### Алгоритм:
1. **Базова ціна**: $200
2. **Сфера бізнесу**: множники 1.0-1.5
3. **Мета сайту**: множники 1.0-1.3
4. **Пріоритети**: ШІ (+40%), SEO (+20%)
5. **Функції**: онлайн оплата (+50%)
6. **Фінальна ціна**: $209-499 (закінчується на "9")

### Терміни виконання:
- **Лендінг**: 2 дні
- **Складні проекти**: до 3 днів
- **Додаткові функції**: +1 день

## 🎨 Дизайн особливості

### Головна сторінка:
- 🌈 **Анімовані градієнти** (фіолетовий → білий)
- 🎭 **Floating cards** з smooth анімаціями
- 📱 **iOS Safari** оптимізація
- ⚡ **Smooth scroll** та магнітні кнопки

### Опитувальник:
- 📊 **6-кроковий процес** з прогрес-баром
- ✅ **Валідація в реальному часі**
- 🎨 **Компактний дизайн** з анімаціями
- 📱 **2x2 сітка** для mobile benefits

### Результати:
- 💰 **Анімація ціни** з ease-out
- 🎯 **Персоналізовані рекомендації**
- 📋 **Візуальні деталі** проекту
- 🎨 **CTA форма** з градієнтами

## 🔧 API Endpoints

| Метод | URL | Опис |
|-------|-----|------|
| `GET` | `/` | Лендінг сторінка |
| `POST` | `/process/` | Обробка опитувальника |
| `GET` | `/result/<id>/` | Результати з ID |
| `POST` | `/submit-contact/` | Відправка контактної форми |
| `GET` | `/admin/` | Адмін панель |

## 🔐 Безпека

- ✅ **CSRF захист** для всіх форм
- 🔒 **SSL/HTTPS** redirect в production
- 🛡️ **Security headers** (HSTS, XSS protection)
- 🔑 **SECRET_KEY** з environment variables
- 🚫 **DEBUG=False** в production

## 🐛 Виправлені проблеми

- ❌ **Видалено дублювання** функції `generateAdvancedMockup`
- ❌ **Оптимізовано CSS** без повторень
- ❌ **Виправлено conflicts** з Bootstrap
- ❌ **Оптимізовано** mobile benefits layout
- ❌ **Очищено** від deadcode

## 📈 Performance

- ⚡ **Мінімізований CSS/JS**
- 🖼️ **Lazy loading** зображень
- 📦 **Whitenoise** для статичних файлів
- 🗜️ **Compressed assets** в production
- 📱 **Mobile-first** підхід

## 🌍 Майбутні плани

- 🌐 **Мультимовність** (UK/EN/RU)
- 📧 **Email інтеграція**
- 🤖 **Telegram бот** notifications
- 📊 **Google Analytics** інтеграція
- 🎨 **A/B тестування**

## 🤝 Внесок у розробку

1. Fork репозиторій
2. Створіть feature branch (`git checkout -b feature/amazing-feature`)
3. Commit зміни (`git commit -m 'Add amazing feature'`)
4. Push до branch (`git push origin feature/amazing-feature`)
5. Відкрийте Pull Request

## 📝 Ліцензія

Цей проект створено для PrometeyLabs. Всі права захищені.

## 📞 Контакти

- **Telegram**: [@prometeylabs](https://t.me/prometeylabs)
- **Сайт**: [prometeylabs.com](https://www.prometeylabs.com/uk/)
- **Email**: info@prometeylabs.com

---

💙💛 **Створено з любов'ю в Україні** | © 2024 PrometeyLabs 