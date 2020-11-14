import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST


@ensure_csrf_cookie
def set_csrf_token(request):
    return JsonResponse({"details": "CSRF cookie set"})


@require_POST
def login_view(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    if username is None or password is None:
        return JsonResponse({
            "errors": {
                "__all__": "Please enter both username and password"
            }
        }, status=400)
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"detail": "Success"})
    return JsonResponse(
        {"detail": "Invalid credentials"},
        status=400,
    )


def signup_view(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    password1 = data.get('password1')
    if username is None or password is None or password1 is None:
        return JsonResponse({
            "errors": {
                "__all__": "Please enter both username and password and password1."
            }
        }, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({
            "errors": {
                "__all__": "User with this username already exists."
            }
        }, status=400)
    user = User.objects.create_user(username=username, password=password)
    user.save()
    login(request, user)
    return JsonResponse({"details": "You've successfully created an account and logged in."})


def logout_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"detail": "You're not logged in."})

    logout(request)
    return JsonResponse({"detail": "Successfully logged out."})


def protected_view(request):
    if request.user.is_authenticated:
        return JsonResponse({"detail": "Super secret information. Your username is: " + request.user.username})
    else:
        return JsonResponse({"detail": "You are not logged in."})
