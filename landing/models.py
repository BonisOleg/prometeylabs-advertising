from django.db import models
from django.utils import timezone


class QuestionnaireResult(models.Model):
    # Основна інформація
    name = models.CharField(max_length=100, blank=True, verbose_name="Ім'я")
    email = models.EmailField(blank=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    
    # Питання опитувальника - нова структура
    business_sphere = models.CharField(
        max_length=50,
        choices=[
            ('goods', 'Товари (інтернет-магазин, каталог)'),
            ('services', 'Послуги (клініка, салон, студія)'),
            ('education', 'Освіта / онлайн-курси'),
            ('personal_brand', 'Особистий бренд'),
            ('startup', 'Стартап / ІТ продукт'),
        ],
        blank=False,
        verbose_name="Сфера бізнесу"
    )
    
    main_goal = models.CharField(
        max_length=50,
        choices=[
            ('sales', 'Продажі / заявки'),
            ('presentation', 'Презентація бізнесу'),
            ('blog_expertise', 'Блог + експертність'),
            ('landing_ads', 'Лендінг під рекламу'),
        ],
        blank=False,
        verbose_name="Головна мета сайту"
    )
    
    priorities = models.JSONField(
        default=list,
        verbose_name="Що найважливіше"
    )
    
    traffic_sources = models.JSONField(
        default=list,
        verbose_name="Джерела трафіку"
    )
    
    needed_features = models.JSONField(
        default=list,
        verbose_name="Потрібні функції"
    )
    
    # Результати розрахунків
    estimated_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Розрахункова ціна"
    )
    
    estimated_days = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Терміни (дні)"
    )
    
    functionality = models.TextField(
        blank=True,
        verbose_name="Рекомендований функціонал"
    )
    
    style = models.TextField(
        blank=True,
        verbose_name="Стиль сайту"
    )
    
    integrations = models.TextField(
        blank=True,
        verbose_name="Рекомендовані інтеграції"
    )
    
    recommendations = models.TextField(
        blank=True,
        verbose_name="Загальні рекомендації"
    )
    
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = "Результат опитувальника"
        verbose_name_plural = "Результати опитувальника"
    
    def __str__(self):
        return f"{self.name} - {self.business_sphere} - ${self.estimated_price}"
