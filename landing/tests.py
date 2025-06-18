from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from unittest.mock import patch, MagicMock
import json
from .models import QuestionnaireResult
from .forms import QuestionnaireForm
from .views import send_telegram_message


class QuestionnaireModelTest(TestCase):
    def test_questionnaire_creation(self):
        """Тест створення моделі QuestionnaireResult"""
        questionnaire = QuestionnaireResult.objects.create(
            name='Тест Користувач',
            phone='+380123456789',
            email='test@example.com',
            business_sphere='goods',
            main_goal='sales',
            priorities=['modern_design'],
            traffic_sources=['google_seo'],
            needed_features=['contact_form'],
            estimated_price=299.00,
            estimated_days=3
        )
        
        self.assertEqual(questionnaire.phone, '+380123456789')
        self.assertEqual(questionnaire.email, 'test@example.com')
        self.assertEqual(questionnaire.business_sphere, 'goods')
        self.assertTrue(questionnaire.created_at)


class QuestionnaireFormTest(TestCase):
    def test_valid_form(self):
        """Тест валідної форми"""
        form_data = {
            'name': 'Тест Користувач',
            'phone': '+380123456789',
            'email': 'test@example.com',
            'business_sphere': 'goods',
            'main_goal': 'sales',
            'priorities': ['modern_design'],
            'traffic_sources': ['google_seo'],
            'needed_features': ['contact_form']
        }
        form = QuestionnaireForm(data=form_data)
        if not form.is_valid():
            print("Form errors:", form.errors)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_required(self):
        """Тест невалідної форми без обов'язкових полів"""
        form_data = {
            'email': 'test@example.com',
        }
        form = QuestionnaireForm(data=form_data)
        self.assertFalse(form.is_valid())


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        """Тест головної сторінки"""
        with patch('django.contrib.staticfiles.storage.staticfiles_storage.url', return_value='/static/test.css'):
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'questionnaireForm')

    @patch('landing.views.send_telegram_message')
    def test_process_questionnaire_valid(self, mock_telegram):
        """Тест успішної обробки анкети"""
        mock_telegram.return_value = True
        
        data = {
            'name': 'Тест Користувач',
            'phone': '+380123456789',
            'email': 'test@example.com',
            'business_sphere': 'goods',
            'main_goal': 'sales',
            'priorities': ['modern_design'],
            'traffic_sources': ['google_seo'],
            'needed_features': ['contact_form']
        }
        
        response = self.client.post(
            '/process/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertTrue(QuestionnaireResult.objects.filter(phone='+380123456789').exists())

    def test_process_questionnaire_invalid(self):
        """Тест обробки невалідної анкети"""
        data = {
            'email': 'invalid-email'
        }
        
        response = self.client.post(
            '/process/',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])

    @patch('landing.views.send_telegram_message')
    def test_submit_contact_valid(self, mock_telegram):
        """Тест відправки контактної форми"""
        mock_telegram.return_value = True
        
        data = {
            'name': 'Тест Контакт',
            'telegram_instagram': '@testuser',
            'phone': '+38(050) 123-45-67',
            'estimated_price': '299',
            'estimated_days': '3'
        }
        
        response = self.client.post('/submit-contact/', data)
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])


class TelegramTest(TestCase):
    @patch('requests.post')
    def test_send_telegram_message_success(self, mock_post):
        """Тест успішної відправки в Telegram"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        with patch.object(settings, 'TELEGRAM_BOT_TOKEN', 'test_token'), \
             patch.object(settings, 'TELEGRAM_CHAT_ID', 'test_chat_id'):
            
            result = send_telegram_message("Test message")
            self.assertTrue(result)

    def test_send_telegram_message_no_credentials(self):
        """Тест відправки без налаштувань Telegram"""
        with patch.object(settings, 'TELEGRAM_BOT_TOKEN', ''), \
             patch.object(settings, 'TELEGRAM_CHAT_ID', ''):
            
            result = send_telegram_message("Test message")
            self.assertFalse(result)

    @patch('requests.post')
    def test_send_telegram_message_failure(self, mock_post):
        """Тест помилки відправки в Telegram"""
        mock_post.side_effect = Exception("Network error")
        
        with patch.object(settings, 'TELEGRAM_BOT_TOKEN', 'test_token'), \
             patch.object(settings, 'TELEGRAM_CHAT_ID', 'test_chat_id'):
            
            result = send_telegram_message("Test message")
            self.assertFalse(result)


class URLTest(TestCase):
    def test_urls_resolve(self):
        """Тест що всі URL правильно налаштовані"""
        with patch('django.contrib.staticfiles.storage.staticfiles_storage.url', return_value='/static/test.css'):
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
        
        # Тест що основні URL існують
        from django.urls import resolve
        self.assertEqual(resolve('/').view_name, 'landing_page')
        self.assertEqual(resolve('/process/').view_name, 'process_questionnaire')
