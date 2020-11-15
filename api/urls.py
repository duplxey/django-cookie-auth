from django.urls import path
from . import views

urlpatterns = [
    path('ensure_csrf/', views.ensure_csrf, name='api-ensure-csrf'),
    path('login/', views.login_view, name='api-login'),
    path('signup/', views.signup_view, name='api-signup'),
    path('logout/', views.logout_view, name='api-logout'),
    path('info/', views.info_view, name='api-info'),
]