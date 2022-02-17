from dataclasses import field, fields
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from rest_framework import serializers

from balance.errors import ErrorResponse
from .models import Balance, Transaction, Transfer


User = get_user_model()


OPERATION_DETAILS = (
    "зачисление средств",
    "оплата товаров и услуг",
    "комиссии",
    "прочие списания"

)


class ShowBalanceSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ('amount', 'owner')
        model = Balance

    
class ChangeBalanceSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('sum', 'details')
        model = Transaction

    def validate_sum(self, sum):
        if sum <= 0:
            raise serializers.ValidationError(
                ErrorResponse.INCORRECT_SUM
            )
        return sum

    def validate_details(self, value):
        if value not in OPERATION_DETAILS:
            raise serializers.ValidationError(
                ErrorResponse.INCORRECT_OPERATION
            )
        return value

    
class TransferSerializer(serializers.ModelSerializer):
    sender_id = serializers.IntegerField()
    receiver_id = serializers.IntegerField()
    sum = serializers.DecimalField(decimal_places=2, max_digits=10)

    class Meta:
        model = Transfer
        exclude = ('outcoming', 'incoming')

    def create(self, validated_data):
        sender = User.objects.get(pk=validated_data['sender_id'])
        receiver = User.objects.get(pk=validated_data['receiver_id'])
        sum = validated_data['sum']
        outcoming = Transaction.objects.create(
            user=sender, operation='transfer',
            details=f'transfer to user <id = {receiver.id}>', sum=sum
        )
        incoming = Transaction.objects.create(
            user=receiver, operation='transfer',
            details=f'incoming transfer from user <id = {sender.id}>', sum=sum
        )
        transfer = Transfer.objects.create(
            outcoming=outcoming, incoming=incoming
        )
        return transfer

    def validate_sender_id(self, sender_id):
        if sender_id == "":
            raise serializers.ValidationError(
                ErrorResponse.ID_REQUIRED
        )
        if not isinstance(sender_id, int) or sender_id < 1:
            raise serializers.ValidationError(
                ErrorResponse.INCORRECT_ID
        )
        return sender_id

    def validate_receiver_id(self, receiver_id):
        if receiver_id == "":
            raise serializers.ValidationError(
                ErrorResponse.ID_REQUIRED
        )
        if not isinstance(receiver_id, int) or receiver_id < 1:
            raise serializers.ValidationError(
                ErrorResponse.INCORRECT_ID
        )
        return receiver_id

    def validate_sum(self, sum):
        if sum <= 0:
            raise serializers.ValidationError(
                ErrorResponse.INCORRECT_SUM
            )
        return sum

    def validate(self, data):
        sender_id = data.get('sender_id')
        receiver_id = data.get('receiver_id')
        if sender_id == receiver_id:
            raise serializers.ValidationError(
                ErrorResponse.INCORRECT_TRANSFER_DATA
            )
        return data


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('operation', 'sum', 'details', 'created')
        model = Transaction

        
