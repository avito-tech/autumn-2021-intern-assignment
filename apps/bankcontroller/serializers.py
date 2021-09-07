from rest_framework import serializers

from .models import Wallet, MoneyCard


class CreateMoneyCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = MoneyCard
        fields = (
            'number', 'month',
            'year', 'amount'
        )

    def validate_number(self, value):
        if len(value) < 16:
            raise serializers.ValidationError(
                'Номер карточки не может быть менее 16 символов'
            )
        return value

    def create(self, validated_data):
        wallet = Wallet.objects.get(
            user=validated_data['user']
        )
        wallet.balance += validated_data['amount']
        wallet.save()
        return super().create(validated_data)
