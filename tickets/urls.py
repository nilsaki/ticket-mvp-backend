from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TicketViewSet, register_user

router = DefaultRouter()
router.register(r"tickets", TicketViewSet, basename="tickets")

urlpatterns = [
    path("", include(router.urls)),
    path("register/", register_user),
]