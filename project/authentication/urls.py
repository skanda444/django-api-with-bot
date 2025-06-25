from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    # API endpoints
    path('login/', views.login_api, name='login_api'),
    path('register/', views.register_api, name='register_api'),
    
    # Template-based login
    path('web/login/', views.LoginView.as_view(), name='web_login'),
]