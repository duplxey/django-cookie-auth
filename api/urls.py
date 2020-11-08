from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='api-login'),
    path('signup/', views.login_view, name='api-signup'),
    path('logout/', views.login_view, name='api-logout'),
]