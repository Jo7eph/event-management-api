from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet
from .auth_views import RegisterView

router = DefaultRouter()
router.register(r"events", EventViewSet, basename="event")

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("", include(router.urls)),
]
