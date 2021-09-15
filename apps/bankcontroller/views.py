import decimal

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, response, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from apps.services.pagination import LimitPageNumberPagination
from apps.services.permissions import AdminCreatOrUserRead

from .filters import (ServiceFilter, UserInfoMoneyTransferFilter,
                      UserInfoServiceLsitFilter)
from .models import MoneyCard, MoneyTransfer, Service, ShopService, Wallet
from .serializers import (CreateMoneyCardSerializer,
                          MoneyTransferForUserSerializer, ServiceSerializer,
                          ShopServiceSerializer)

CUREENCY = {
    "USD": 0.39,
    'EUR': 0.33,
    "RUB": 29.14,
    "BYN": 1
}


class CreateMoneyCardView(mixins.CreateModelMixin, viewsets.GenericViewSet):

    queryset = MoneyCard.objects.all()
    serializer_class = CreateMoneyCardSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class ServiceView(viewsets.ModelViewSet):

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [AdminCreatOrUserRead]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ServiceFilter

    def _get_user_or_service(self, request):
        user = request.user
        service = self.get_object()
        return user, service

    @action(
        detail=True,
        methods=['GET'],
        permission_classes=[IsAuthenticated]
    )
    def shop(self, request, pk=None):
        user, service = self._get_user_or_service(request)
        user_balance = Wallet.objects.get(user=user)
        currency = decimal.Decimal(CUREENCY[service.currency])
        service_price = service.price / currency
        if ShopService.objects.filter(user=user, service=service).exists():
            return response.Response(
                f"У Вас уже приобретена услуга {service.name}"
            )
        purchase = user_balance.balance - service_price
        if purchase < 0:
            return response.Response(
                f"У Вас недостаточно средств для покупки {service.name}",
                status=status.HTTP_402_PAYMENT_REQUIRED
            )
        user_balance.balance -= service_price
        user_balance.save()
        shop = ShopService.objects.create(
            user=user,
            service=service
        )
        shop.save()
        return response.Response(
            {'detail': f'Вы успешно купили услугу {service.name}'},
            status=status.HTTP_200_OK
        )


class InfoListShopService(mixins.ListModelMixin, viewsets.GenericViewSet):

    serializer_class = ShopServiceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserInfoServiceLsitFilter
    pagination_class = LimitPageNumberPagination

    def get_queryset(self):
        return ShopService.objects.filter(user=self.request.user)


class InfoListMoneyTransfer(mixins.ListModelMixin, viewsets.GenericViewSet):

    serializer_class = MoneyTransferForUserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserInfoMoneyTransferFilter
    pagination_class = LimitPageNumberPagination

    def get_queryset(self):
        return MoneyTransfer.objects.filter(user_transfer=self.request.user)
