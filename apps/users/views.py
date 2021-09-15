import decimal

from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as BaseUserViewSet
from rest_framework import response, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from apps.bankcontroller.models import MoneyTransfer, Wallet
from apps.bankcontroller.serializers import MoneyTransferSerializer
from apps.services.pagination import LimitPageNumberPagination

from .models import User
from .serializers import InfoSerializer


class UserViewSet(BaseUserViewSet):

    queryset = User.objects.all()
    pagination_class = LimitPageNumberPagination

    def get_serializer_class(self):
        if self.action == 'money_trafic':
            return MoneyTransferSerializer
        return super().get_serializer_class()

    def _get_user_or_service(self, request):
        user_transfer = request.user
        user_received = self.get_object()
        return user_transfer, user_received

    @action(
        detail=True,
        methods=['POST'],
        permission_classes=[IsAuthenticated]
    )
    def money_trafic(self, request, id=None):
        try:
            user_transfer, user_received = self._get_user_or_service(request)
            wallet_user_transfer = Wallet.objects.get(user=user_transfer)
            wallet_user_received = Wallet.objects.get(user=user_received)
            amount = decimal.Decimal(request.POST.get('amount'))
            if wallet_user_transfer.balance - amount < 0:
                return response.Response(
                    {
                        'detail': 'У вас недостаточно средств!!!'
                    }
                )
            wallet_user_transfer.balance -= amount
            wallet_user_transfer.save()
            wallet_user_received.balance += amount
            wallet_user_received.save()
            money_tranfer = MoneyTransfer.objects.create(
                user_transfer=user_transfer,
                user_received=user_received,
                amount=amount
            )
            money_tranfer.save()
            return response.Response(
                {
                    'detail': (
                        f'Вы успешно перевели пользователю '
                        f'{self.get_object()} сумму {amount} BYN'
                    )
                }, status.HTTP_200_OK
            )
        except decimal.InvalidOperation:
            return response.Response({'error': 'Проверьте что Вы ввели'})

    # pagination & filter create
    @action(detail=False, permission_classes=[IsAuthenticated])
    def info_list(self, request):
        return response.Response(InfoSerializer(request.user).data)
