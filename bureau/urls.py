from django.urls import path
from django.contrib.auth import views as auth_views
from .views import ProfileWizard, FORMS, redirect_after_login, thank_you, admin_dashboard, profile_detail

urlpatterns = [
    path('', redirect_after_login, name='home'),
    path('form/', ProfileWizard.as_view(FORMS), name='user_form'),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('thank-you/', thank_you, name='thank_you'),
    path('profile/<int:pk>/', profile_detail, name='profile_detail'),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]