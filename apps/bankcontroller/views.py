from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import MoneyCard
from .serializers import CreateMoneyCardSerializer


class CreateMoneyCardView(CreateAPIView):

    queryset = MoneyCard.objects.all()
    serializer_class = CreateMoneyCardSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
