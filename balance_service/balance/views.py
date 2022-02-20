from django.contrib.auth import get_user_model
from django.db import transaction
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, status, views
from rest_framework.response import Response

from balance.models import Balance, Transaction, Transfer
from balance.errors import (BalanceDoesNotExist, UserDoesNotExist, CurrencyNotFound,
                            ErrorResponse)
from balance.scripts import convert
from balance.serializers import (ShowBalanceSerializer, ChangeBalanceSerializer,
                                TransferSerializer, TransactionSerializer)


User = get_user_model()


class UserBalance(views.APIView):

    def _get_balance(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except Exception as e:
            raise UserDoesNotExist
        try:
            balance = Balance.objects.get(owner=user_id)
        except Exception as e:
            raise BalanceDoesNotExist
        return user, balance

    def _get_or_create_balance(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except Exception as e:
            raise UserDoesNotExist
        balance, status = Balance.objects.get_or_create(owner_id=user_id)
        return user, balance


class ShowBalance(UserBalance):

    def get(self, request, pk):
        user, balance = self._get_balance(pk)
        currency = self.request.query_params.get('currency')
        if currency:
            try:
                balance.amount = convert(currency, balance.amount)
            except CurrencyNotFound:
                return Response(ErrorResponse.INCORRECT_CURRENCY,
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        serializer = ShowBalanceSerializer(balance)        
        return Response(serializer.data, status=status.HTTP_200_OK)


class RefillBalance(UserBalance):

    def post(self, request, pk):
        serializer = ChangeBalanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, balance = self._get_or_create_balance(pk)
        except UserDoesNotExist:
            return Response(ErrorResponse.USER_DOES_NOT_EXIST,
                                status=status.HTTP_404_NOT_FOUND)
        sum = serializer.validated_data['sum']
        with transaction.atomic():
            balance.amount += sum
            balance.save()
            serializer.save(user=user, operation='refill')
            serializer = ShowBalanceSerializer(balance)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
                
class WithdrawBalance(UserBalance):

    def post(self, request, pk):
        try:
            user, balance = self._get_balance(pk)
        except UserDoesNotExist:
            return Response(ErrorResponse.USER_DOES_NOT_EXIST,
                                status=status.HTTP_404_NOT_FOUND)
        except BalanceDoesNotExist:
            return Response(ErrorResponse.NO_BANK_ACCOUNT,
                                status=status.HTTP_404_NOT_FOUND)
        serializer = ChangeBalanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sum = serializer.validated_data['sum']
        if balance.amount < sum:
                return Response(ErrorResponse.NOT_ENOUGH_FUNDS,
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        with transaction.atomic():
            balance.amount -= sum
            balance.save()
            serializer.save(user=user, operation='withdraw')
            serializer = ShowBalanceSerializer(balance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TransferView(UserBalance):

    def post(self, request):
        serializer = TransferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sender_id = serializer.validated_data['sender_id']
        try:
            sender, sender_balance = self._get_balance(sender_id)
        except UserDoesNotExist:
            return Response(ErrorResponse.USER_DOES_NOT_EXIST,
                                status=status.HTTP_404_NOT_FOUND)
        except BalanceDoesNotExist:
            return Response(ErrorResponse.NO_BANK_ACCOUNT,
                        status=status.HTTP_404_NOT_FOUND)
        sum = serializer.validated_data['sum']
        if sender_balance.amount < sum:
                return Response(ErrorResponse.NOT_ENOUGH_FUNDS,
                                status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        receiver_id = serializer.validated_data['receiver_id']
        try:
            receiver, receiver_balance = self._get_or_create_balance(receiver_id)
        except UserDoesNotExist:
            return Response(ErrorResponse.USER_DOES_NOT_EXIST,
                                status=status.HTTP_404_NOT_FOUND)
        with transaction.atomic():
            sender_balance.amount -= sum
            sender_balance.save()
            receiver_balance.amount += sum
            receiver_balance.save()
            serializer.save()
        return Response(data={
            'sender_id': sender.id,
            'receiver_id': receiver.id,
            'balance': sender_balance.amount},
            status=status.HTTP_200_OK
        )
        

class TransactionHistory(generics.ListAPIView):
    serializer_class = TransactionSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('sum', 'created')

    def get_queryset(self):
        user_id = self.kwargs.get('pk')
        user = get_object_or_404(User, id=user_id)
        return user.transactions.all()
