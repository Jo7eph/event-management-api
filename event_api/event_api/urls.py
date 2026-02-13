from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

def home(request):
    return JsonResponse({
        "message": "Event API is running",
        "admin": "/admin/",
        "api": "/api/",
        "register": "/api/auth/register/",
        "token": "/api/auth/token/",
        "upcoming": "/api/events/upcoming/",
    })

urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),

    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("api/", include("events.urls")),
]
