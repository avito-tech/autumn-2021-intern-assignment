from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import response, status

from .models import MoneyCard, Service, Wallet, ShopService
from .serializers import CreateMoneyCardSerializer, ServiceSerializer, ShopServiceSerializer
from ..services.permissions import AdminCreatOrUserRead


class CreateMoneyCardView(CreateAPIView):

    queryset = MoneyCard.objects.all()
    serializer_class = CreateMoneyCardSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class ServiceView(viewsets.ModelViewSet):

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [AdminCreatOrUserRead]

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
        service_price = service.price
        if ShopService.objects.filter(user=user, service=service).exists():
            return response.Response(
                f"У Вас уже приобретена услуга {service.name}"
            )
        purchase = user_balance.balance - service_price
        if purchase < 0:
            return response.Response(
                f"У Вас недостаточна средств для покупки {service.name}",
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


