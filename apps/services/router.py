from rest_framework.routers import DefaultRouter
from django.urls import path

from ..bankcontroller.views import CreateMoneyCardView
from ..users.views import UserViewSet

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('create_money_card/', CreateMoneyCardView.as_view(),
         name='create-money-card')
] + router.urls
