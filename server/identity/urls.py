"""
URLs para autenticação e gerenciamento de usuários.
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'identity'

urlpatterns = [
    # Login/Logout (usando views padrão do Django)
    path('login/', auth_views.LoginView.as_view(template_name='identity/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Registro
    path('register/', views.register_view, name='register'),
]
