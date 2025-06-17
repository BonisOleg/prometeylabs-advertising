from django.contrib import admin
from .models import QuestionnaireResult


@admin.register(QuestionnaireResult)
class QuestionnaireResultAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'email', 'business_sphere', 'main_goal', 
        'estimated_price', 'estimated_days', 'created_at'
    ]
    list_filter = [
        'business_sphere', 'main_goal', 'created_at'
    ]
    search_fields = ['name', 'email', 'phone']
    readonly_fields = ['created_at', 'estimated_price', 'estimated_days']
    
    fieldsets = (
        ('Основна інформація', {
            'fields': ('name', 'email', 'phone', 'created_at')
        }),
        ('Деталі проекту', {
            'fields': (
                'business_sphere', 'main_goal', 'priorities',
                'traffic_sources', 'needed_features'
            )
        }),
        ('Результати аналізу', {
            'fields': (
                'estimated_price', 'estimated_days', 'functionality',
                'style', 'integrations', 'recommendations'
            )
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('priorities', 'traffic_sources', 'needed_features')
        return self.readonly_fields
