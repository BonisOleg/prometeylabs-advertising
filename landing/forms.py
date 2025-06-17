from django import forms
from .models import QuestionnaireResult


class QuestionnaireForm(forms.ModelForm):
    
    # Перевизначаємо поля щоб прибрати порожні варіанти
    business_sphere = forms.ChoiceField(
        choices=[
            ('goods', 'Товари (інтернет-магазин, каталог)'),
            ('services', 'Послуги (клініка, салон, студія)'),
            ('education', 'Освіта / онлайн-курси'),
            ('personal_brand', 'Особистий бренд'),
            ('startup', 'Стартап / ІТ продукт'),
        ],
        widget=forms.RadioSelect(attrs={'class': 'form-radio'}),
        label='У якій сфері працює ваш бізнес?'
    )
    
    main_goal = forms.ChoiceField(
        choices=[
            ('sales', 'Продажі / заявки'),
            ('presentation', 'Презентація бізнесу'),
            ('blog_expertise', 'Блог + експертність'),
            ('landing_ads', 'Лендінг під рекламу'),
        ],
        widget=forms.RadioSelect(attrs={'class': 'form-radio'}),
        label='Яка ваша головна мета сайту?'
    )
    
    # Питання 3: Що найважливіше (множинний вибір)
    PRIORITIES_CHOICES = [
        ('modern_design', 'Сучасний дизайн'),
        ('fast_loading', 'Швидке завантаження'),
        ('seo_promotion', 'SEO та просування'),
        ('ai_integration', 'Інтеграція ШІ'),
        ('client_simplicity', 'Простота для клієнта'),
    ]
    
    priorities_selected = forms.MultipleChoiceField(
        choices=PRIORITIES_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'priority-checkbox'}),
        label="🧠 Що для вас найважливіше? (можна обрати декілька)"
    )
    
    # Питання 4: Джерела трафіку (множинний вибір)
    TRAFFIC_CHOICES = [
        ('instagram_tiktok', 'Instagram / TikTok'),
        ('google_seo', 'Google реклама / SEO'),
        ('referrals', 'Рекомендації / сарафанне радіо'),
        ('email_content', 'Email / контент'),
    ]
    
    traffic_sources_selected = forms.MultipleChoiceField(
        choices=TRAFFIC_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'traffic-checkbox'}),
        label="📱 Як плануєте залучати трафік? (можна обрати декілька)"
    )
    
    # Питання 5: Потрібні функції (множинний вибір)
    FEATURES_CHOICES = [
        ('online_payment', 'Онлайн-оплата / кошик'),
        ('contact_form', 'Форма заявки + автоemail'),
        ('blog', 'Онлайн-блог'),
        ('calendar_booking', 'Календар / запис'),
        ('other', 'Інший варіант'),
    ]
    
    features_selected = forms.MultipleChoiceField(
        choices=FEATURES_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'feature-checkbox'}),
        label="🔧 Які функції вам потрібні? (можна обрати декілька)"
    )
    
    class Meta:
        model = QuestionnaireResult
        fields = [
            'name', 'email', 'phone', 'business_sphere', 'main_goal'
        ]
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-input',
                'placeholder': 'Введіть ваше ім\'я'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-input',
                'placeholder': 'your@email.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control form-input',
                'placeholder': '+380XXXXXXXXX'
            }),
        }
        
        labels = {
            'name': 'Як вас звати?',
            'email': 'Ваш email для зв\'язку',
            'phone': 'Телефон (опціонально)',
        }
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # Зберігаємо обрані варіанти
        instance.priorities = self.cleaned_data.get('priorities_selected', [])
        instance.traffic_sources = self.cleaned_data.get('traffic_sources_selected', [])
        instance.needed_features = self.cleaned_data.get('features_selected', [])
        
        if commit:
            instance.save()
        return instance 