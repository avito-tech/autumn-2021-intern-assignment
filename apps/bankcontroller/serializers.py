from rest_framework import serializers

from .models import ShopService, Wallet, MoneyCard, Service


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


class ServiceSerializer(serializers.ModelSerializer):

    purchased = serializers.SerializerMethodField(
        'service_was_purchased_by_the_user')

    class Meta:
        model = Service
        fields = (
            'name',
            'id',
            'description',
            'price',
            'purchased'
        )

    def service_was_purchased_by_the_user(self, obj):
        try:
            request = self.context.get('request')
            if request is None or request.user.is_anonymous:
                return False
            return ShopService.objects.filter(
                service=obj,
                user=request.user
            ).exists()
        except TypeError:
            return False


class ShopServiceSerializer(serializers.ModelSerializer):

    service = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = ShopService
        fields = (
            'service',
            'date'
        )
