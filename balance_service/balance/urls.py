from django.urls import include, path
from rest_framework.routers import DefaultRouter

from balance.views import (ShowBalance, RefillBalance,
                        WithdrawBalance, TransferView,
                        TransactionHistory)


urlpatterns = [
    path('v1/balance/<int:pk>/', ShowBalance.as_view()),
    path('v1/balance/<int:pk>/refill/', RefillBalance.as_view()),
    path('v1/balance/<int:pk>/withdraw/', WithdrawBalance.as_view()),
    path('v1/transfer/', TransferView.as_view()),
    path('v1/transactions/<int:pk>/details/', TransactionHistory.as_view()),
]