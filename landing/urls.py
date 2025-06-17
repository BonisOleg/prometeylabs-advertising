from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='landing_page'),
    path('process/', views.process_questionnaire, name='process_questionnaire'),
    path('submit-contact/', views.submit_contact, name='submit_contact'),
    path('result/<int:result_id>/', views.result_page, name='result_page'),
] 