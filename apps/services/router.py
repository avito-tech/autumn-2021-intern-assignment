from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.bankcontroller.views import CreateMoneyCardView, ServiceView
from apps.users.views import UserViewSet

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='users')
router.register(r'services', ServiceView, basename='services')

urlpatterns = [
    path('create_money_card/', CreateMoneyCardView.as_view(),
         name='create-money-card')
] + router.urls
