from django.urls import path
from . import views

urlpatterns = [
    path('ensure_csrf/', views.set_csrf_token, name='api-ensure-csrf'),
    path('login/', views.login_view, name='api-login'),
    path('signup/', views.login_view, name='api-signup'),
    path('logout/', views.login_view, name='api-logout'),
    path('protected/', views.protected_view, name='api-protected'),
]