from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import random
from .forms import QuestionnaireForm
from .models import QuestionnaireResult


def index(request):
    """Головна сторінка лендінгу"""
    form = QuestionnaireForm()
    return render(request, 'landing/index.html', {'form': form})


def calculate_price_and_timeline(questionnaire_data):
    """Розрахунок приблизної вартості сайту та термінів"""
    base_price = 200  # Базова ціна
    base_days = 1  # Базові терміни
    
    business_sphere = questionnaire_data.get('business_sphere', '')
    main_goal = questionnaire_data.get('main_goal', '')
    priorities = questionnaire_data.get('priorities', [])
    traffic_sources = questionnaire_data.get('traffic_sources', [])
    features = questionnaire_data.get('needed_features', [])
    
    # Коефіцієнти за сферою бізнесу
    sphere_multipliers = {
        'goods': 1.4,  # Інтернет-магазин складніший
        'services': 1.1,
        'education': 1.3,  # Онлайн-курси потребують більше функцій
        'personal_brand': 1.0,  # Найпростіше
        'startup': 1.5,  # ІТ продукт найскладніший
    }
    
    # Коефіцієнти за головною метою
    goal_multipliers = {
        'sales': 1.3,  # Продажі потребують більше функцій
        'presentation': 1.0,  # Презентація простіше
        'blog_expertise': 1.2,  # Блог середньої складності
        'landing_ads': 1.1,  # Лендінг під рекламу
    }
    
    # Додаткові коефіцієнти за пріоритетами
    priority_multipliers = {
        'modern_design': 1.15,
        'fast_loading': 1.1,
        'seo_promotion': 1.2,
        'ai_integration': 1.4,  # ШІ додає значну вартість
        'client_simplicity': 1.05,
    }
    
    # Коефіцієнти за джерелами трафіку
    traffic_multipliers = {
        'instagram_tiktok': 1.1,  # Потребує оптимізації під соцмережі
        'google_seo': 1.25,  # SEO складніше
        'referrals': 1.0,
        'email_content': 1.15,
    }
    
    # Коефіцієнти за функціями
    feature_multipliers = {
        'online_payment': 1.5,  # Онлайн-оплата значно ускладнює
        'contact_form': 1.1,
        'blog': 1.2,
        'calendar_booking': 1.3,  # Календар складний
        'other': 1.1,  # Інший варіант може потребувати додаткової роботи
    }
    
    # Розрахунок базової ціни
    price = base_price
    days = base_days
    
    # Застосовуємо множники
    price *= sphere_multipliers.get(business_sphere, 1.0)
    price *= goal_multipliers.get(main_goal, 1.0)
    
    # Пріоритети
    for priority in priorities:
        price *= priority_multipliers.get(priority, 1.0)
        if priority in ['ai_integration', 'seo_promotion']:
            days += 1  # Складні функції додають день
    
    # Джерела трафіку
    for source in traffic_sources:
        price *= traffic_multipliers.get(source, 1.0)
        if source == 'google_seo':
            days += 1  # SEO додає день
    
    # Функції
    for feature in features:
        price *= feature_multipliers.get(feature, 1.0)
        if feature in ['online_payment', 'calendar_booking']:
            days += 1  # Складні функції додають день
    
    # Обмежуємо ціну в межах $200-500
    price = max(200, min(500, price))
    
    # Терміни залежно від типу сайту
    if main_goal == 'landing_ads':
        days = 2  # Лендінг швидше
    else:
        days = 3  # Інші типи сайтів
    
    # Додаткові дні за складність
    if business_sphere in ['goods', 'startup']:
        days = min(days + 1, 3)  # Максимум 3 дні
    
    if 'ai_integration' in priorities or 'online_payment' in features:
        days = min(days + 1, 3)  # Максимум 3 дні
    
    # Генеруємо ціни що закінчуються на "9" залежно від складності
    # Створюємо список можливих цін від 209 до 499 з кроком 10 (всі закінчуються на 9)
    possible_prices = [209, 219, 229, 239, 249, 259, 269, 279, 289, 299, 
                      309, 319, 329, 339, 349, 359, 369, 379, 389, 399,
                      409, 419, 429, 439, 449, 459, 469, 479, 489, 499]
    
    # Знаходимо найближчу ціну що закінчується на "9"
    target_price = max(209, min(499, price))  # Обмежуємо в межах 209-499
    
    # Знаходимо найближчу ціну з нашого списку
    closest_price = min(possible_prices, key=lambda x: abs(x - target_price))
    price = closest_price
    
    return round(price, 0), days


def generate_personalized_result(questionnaire_data, price, days):
    """Генерація персоналізованого результату"""
    business_sphere = questionnaire_data.get('business_sphere', '')
    main_goal = questionnaire_data.get('main_goal', '')
    priorities = questionnaire_data.get('priorities', [])
    traffic_sources = questionnaire_data.get('traffic_sources', [])
    features = questionnaire_data.get('needed_features', [])
    
    # Генерація функціоналу
    functionality_map = {
        'goods': ['Каталог товарів', 'Кошик', 'Система оплати', 'Фільтри пошуку'],
        'services': ['Портфоліо робіт', 'Форма заявки', 'Опис послуг', 'Відгуки клієнтів'],
        'education': ['Каталог курсів', 'Система реєстрації', 'Особистий кабінет', 'Сертифікати'],
        'personal_brand': ['Про мене', 'Портфоліо', 'Блог', 'Контакти'],
        'startup': ['Опис продукту', 'Демо версія', 'Підписка на новини', 'Інвестори'],
    }
    
    functionality = functionality_map.get(business_sphere, ['Головна сторінка', 'Про нас', 'Контакти'])
    
    # Додаємо функції відповідно до обраних
    if 'online_payment' in features:
        functionality.append('Онлайн оплата')
    if 'contact_form' in features:
        functionality.append('Форма заявки з автоemail')
    if 'blog' in features:
        functionality.append('Блог з можливістю публікацій')
    if 'calendar_booking' in features:
        functionality.append('Система онлайн-запису')
    if 'other' in features:
        functionality.append('Індивідуальні функції за вашими потребами')
    
    # Генерація стилю
    style_map = {
        'goods': 'Сучасний e-commerce дизайн з акцентом на товари',
        'services': 'Елегантний корпоративний стиль з портфоліо',
        'education': 'Освітній дизайн з яскравими акцентами',
        'personal_brand': 'Мінімалістичний персональний стиль',
        'startup': 'Інноваційний tech дизайн з градієнтами',
    }
    
    style = style_map.get(business_sphere, 'Універсальний сучасний дизайн')
    
    if 'modern_design' in priorities:
        style += ' з сучасними трендами'
    if 'client_simplicity' in priorities:
        style += ' з акцентом на простоту використання'
    
    # Генерація інтеграцій
    integrations = []
    
    if 'instagram_tiktok' in traffic_sources:
        integrations.append('Інтеграція з Instagram та TikTok')
    if 'google_seo' in traffic_sources:
        integrations.append('Google Analytics та Search Console')
    if 'email_content' in traffic_sources:
        integrations.append('Email маркетинг (MailChimp/SendGrid)')
    
    if 'ai_integration' in priorities:
        integrations.append('ШІ чат-бот для автоматичних відповідей')
        integrations.append('ШІ аналіз поведінки користувачів')
    
    if 'online_payment' in features:
        integrations.append('Платіжні системи (LiqPay, Fondy)')
    
    if 'seo_promotion' in priorities:
        integrations.append('SEO оптимізація та швидкість')
    
    if not integrations:
        integrations = ['Базові інтеграції з соцмережами', 'Google Analytics']
    
    # Загальні рекомендації
    recommendations = []
    
    if business_sphere == 'goods':
        recommendations.append('🛒 Додайте систему знижок та акцій для збільшення продажів')
        recommendations.append('📊 Налаштуйте аналітику для відстеження конверсій')
    elif business_sphere == 'services':
        recommendations.append('⭐ Додайте секцію відгуків клієнтів для підвищення довіри')
        recommendations.append('📞 Створіть зручну форму для консультацій')
    elif business_sphere == 'education':
        recommendations.append('🎓 Розробіть систему прогресу студентів')
        recommendations.append('💬 Додайте форум або чат для спілкування')
    elif business_sphere == 'personal_brand':
        recommendations.append('📝 Регулярно оновлюйте блог для SEO')
        recommendations.append('🎯 Створіть лід-магніт для збору контактів')
    elif business_sphere == 'startup':
        recommendations.append('🚀 Додайте landing page для кожної функції продукту')
        recommendations.append('📈 Налаштуйте A/B тестування')
    
    if main_goal == 'sales':
        recommendations.append('💰 Оптимізуйте воронку продажів')
    if main_goal == 'presentation':
        recommendations.append('🎨 Зробіть акцент на візуальній презентації')
    
    if 'fast_loading' in priorities:
        recommendations.append('⚡ Оптимізуємо швидкість завантаження до 2 секунд')
    
    return {
        'functionality': '\n'.join(f'• {item}' for item in functionality),
        'style': style,
        'integrations': '\n'.join(f'• {item}' for item in integrations),
        'recommendations': recommendations
    }


@csrf_exempt
@require_http_methods(["POST"])
def process_questionnaire(request):
    """Обробка форми опитувальника"""
    try:

        # Отримання даних з POST
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST.dict()
            # Обробляємо checkbox fields
            data['priorities'] = request.POST.getlist('priorities_selected')
            data['traffic_sources'] = request.POST.getlist('traffic_sources_selected')
            data['needed_features'] = request.POST.getlist('features_selected')
        
        # Створюємо форму тільки з основними полями
        form_data = {k: v for k, v in data.items() if k not in ['priorities', 'traffic_sources', 'needed_features']}
        form = QuestionnaireForm(form_data)

        
        # Перевіряємо обов'язкові поля вручну
        if not data.get('business_sphere') or not data.get('main_goal'):
            return JsonResponse({
                'success': False,
                'error': 'Будь ласка, оберіть сферу бізнесу та головну мету'
            })
        
        # Обробляємо форму навіть якщо name/email порожні
        if form.is_valid() or not any(field in form.errors for field in ['business_sphere', 'main_goal']):
            # Підготовка даних для розрахунків
            questionnaire_data = {
                'business_sphere': data.get('business_sphere'),
                'main_goal': data.get('main_goal'),
                'priorities': data.get('priorities', []),
                'traffic_sources': data.get('traffic_sources', []),
                'needed_features': data.get('needed_features', [])
            }
            
            # Розрахунок ціни та термінів
            calculated_price, estimated_days = calculate_price_and_timeline(questionnaire_data)
            
            # Генерація персоналізованого результату
            personalized_result = generate_personalized_result(
                questionnaire_data, calculated_price, estimated_days
            )
            
            # Створюємо результат вручну, оскільки форма може бути неповною
            result = QuestionnaireResult(
                name=data.get('name', 'Анонімний користувач'),
                email=data.get('email', 'noemail@example.com'),
                phone=data.get('phone', ''),
                business_sphere=data.get('business_sphere'),
                main_goal=data.get('main_goal'),
                priorities=data.get('priorities', []),
                traffic_sources=data.get('traffic_sources', []),
                needed_features=data.get('needed_features', []),
                estimated_price=calculated_price,
                estimated_days=estimated_days,
                functionality=personalized_result['functionality'],
                style=personalized_result['style'],
                integrations=personalized_result['integrations'],
                recommendations='\n'.join(personalized_result['recommendations'])
            )
            result.save()
            
            # Повертаємо результат
            response_data = {
                'success': True,
                'estimated_price': int(calculated_price),
                'estimated_days': estimated_days,
                'functionality': personalized_result['functionality'],
                'style': personalized_result['style'],
                'integrations': personalized_result['integrations'],
                'recommendations': personalized_result['recommendations'],
                'result_id': result.id,
            }
            
            return JsonResponse(response_data)
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
            
    except Exception as e:

        return JsonResponse({
            'success': False,
            'error': str(e)
        })


def result_page(request, result_id):
    """Сторінка з результатами"""
    try:
        result = QuestionnaireResult.objects.get(id=result_id)
        recommendations_list = result.recommendations.split('\n') if result.recommendations else []
        
        context = {
            'result': result,
            'recommendations': recommendations_list,
        }
        return render(request, 'landing/result.html', context)
    except QuestionnaireResult.DoesNotExist:
        return redirect('landing_page')


@require_http_methods(["POST"])
def submit_contact(request):
    try:
        # Отримуємо дані з форми
        contact_name = request.POST.get('name', '').strip()
        telegram_instagram = request.POST.get('telegram_instagram', '').strip()
        contact_phone = request.POST.get('phone', '').strip()
        
        # Отримуємо дані розрахунку
        estimated_price = request.POST.get('estimated_price', '')
        estimated_days = request.POST.get('estimated_days', '')
        functionality = request.POST.get('functionality', '')
        style = request.POST.get('style', '')
        integrations = request.POST.get('integrations', '')
        recommendations = request.POST.get('recommendations', '')
        
        # Валідація обов'язкових полів
        if not contact_name or not telegram_instagram:
            return JsonResponse({
                'success': False,
                'error': 'Ім\'я та telegram/instagram є обов\'язковими полями'
            })
        
        # Валідація telegram/instagram формату
        import re
        if not re.match(r'^@[a-zA-Z0-9_]{3,}$', telegram_instagram):
            return JsonResponse({
                'success': False,
                'error': 'Введіть коректний @telegram або @instagram нікнейм'
            })
        
        # Валідація телефону (якщо введений)
        if contact_phone and not re.match(r'^\+38\(\d{3}\) \d{3}-\d{2}-\d{2}$', contact_phone):
            return JsonResponse({
                'success': False,
                'error': 'Введіть коректний номер телефону у форматі +38(0__) ___-__-__'
            })
        
        # Тут можна додати логіку збереження в базу даних
        # або відправки email/повідомлення в Telegram
        
        # Для прикладу, просто логуємо дані
        contact_data = {
            'name': contact_name,
            'telegram_instagram': telegram_instagram,
            'phone': contact_phone,
            'estimated_price': estimated_price,
            'estimated_days': estimated_days,
            'functionality': functionality,
            'style': style,
            'integrations': integrations,
            'recommendations': recommendations
        }
        print(f"Нова заявка: {contact_data}")
        
        # Можна додати відправку в Telegram або email
        # send_telegram_notification(contact_data)
        # send_email_notification(contact_data)
        
        return JsonResponse({
            'success': True,
            'message': 'Дякуємо! Ми зв\'яжемося з вами найближчим часом.'
        })
        
    except Exception as e:
        print(f"Помилка при обробці контактної форми: {e}")
        return JsonResponse({
            'success': False,
            'error': 'Виникла помилка при відправці. Спробуйте ще раз.'
        })
