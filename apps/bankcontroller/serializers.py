from rest_framework import serializers

from .models import MoneyCard, Service, ShopService, Wallet


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
            'currency',
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


class ServiceInShopServiceSerializer(serializers.ModelSerializer):

    price = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = (
            'name',
            'price'
        )

    def get_price(self, obj):
        return f"{obj.price} {obj.currency}"


class ShopServiceSerializer(serializers.ModelSerializer):

    service = ServiceInShopServiceSerializer(read_only=True)
    date = serializers.SerializerMethodField()

    class Meta:
        model = ShopService
        fields = (
            'service',
            'date'
        )

    def get_date(self, obj):
        return f' Куплено: {obj.date.strftime("%d.%m.%Y")} в {obj.date.strftime("%H:%I")}'
