from apps.bankcontroller.views import CreateMoneyCardView, ServiceView
from apps.users.views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='users')
router.register(r'services', ServiceView, basename='services')
router.register(r'create_money_card', CreateMoneyCardView,
                basename='create-money-card')

urlpatterns = [] + router.urls
