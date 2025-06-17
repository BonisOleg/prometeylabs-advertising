"""
Налаштування змінних середовища для різних етапів розробки
"""

import os

def get_env_variable(var_name, default=None, required=False):
    """
    Отримує змінну середовища з можливістю встановлення значення за замовчуванням
    """
    value = os.environ.get(var_name, default)
    
    if required and value is None:
        raise ValueError(f"Змінна середовища {var_name} є обов'язковою")
    
    return value

def is_production():
    """
    Перевіряє чи додаток працює в production середовищі
    """
    return get_env_variable('DJANGO_ENV', 'development').lower() == 'production'

def is_development():
    """
    Перевіряє чи додаток працює в development середовищі
    """
    return not is_production()

# Налаштування для різних сервісів
DATABASE_URL = get_env_variable('DATABASE_URL')
REDIS_URL = get_env_variable('REDIS_URL')

# Email налаштування
EMAIL_HOST = get_env_variable('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(get_env_variable('EMAIL_PORT', '587'))
EMAIL_HOST_USER = get_env_variable('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = get_env_variable('EMAIL_USE_TLS', 'True').lower() == 'true'

# Telegram Bot налаштування
TELEGRAM_BOT_TOKEN = get_env_variable('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = get_env_variable('TELEGRAM_CHAT_ID')

# Зовнішні сервіси
GOOGLE_ANALYTICS_ID = get_env_variable('GOOGLE_ANALYTICS_ID')
FACEBOOK_PIXEL_ID = get_env_variable('FACEBOOK_PIXEL_ID') 