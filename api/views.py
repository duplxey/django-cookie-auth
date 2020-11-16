import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from djangocookieauth import settings


@ensure_csrf_cookie
def ensure_csrf(request):
    return JsonResponse({"detail": "CSRF cookie set."})


def cors_view(request):
    return JsonResponse({
        "CORS_ALLOWED_ORIGINS ": settings.CORS_ALLOWED_ORIGINS,
        "CSRF_TRUSTED_ORIGINS  ": settings.CSRF_TRUSTED_ORIGINS,
    })


@require_POST
def login_view(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    if username is None or password is None:
        return JsonResponse({"detail": "Please provide both username & password."}, status=400)

    user = authenticate(username=username, password=password)

    if user is None:
        return JsonResponse({"detail": "Invalid credentials."}, status=400)

    login(request, user)
    return JsonResponse({"detail": "Successfully logged in."})


@require_POST
def signup_view(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    password1 = data.get('password1')

    if username is None or password is None or password1 is None:
        return JsonResponse({"detail": "Please provide both username, password & password1."}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({"detail": "User with this username already exists."}, status=400)

    user = User.objects.create_user(username=username, password=password)
    user.save()

    login(request, user)
    return JsonResponse({"detail": "You've successfully created an account and logged in."})


@require_POST
def logout_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"detail": "You're not logged in."}, status=400)

    logout(request)
    return JsonResponse({"detail": "Successfully logged out."})


def info_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"loggedIn": False})

    return JsonResponse({"loggedIn": True, "username": request.user.username})

