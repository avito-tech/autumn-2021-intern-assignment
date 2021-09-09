from rest_framework import serializers
from .models import User

from ..bankcontroller.models import Wallet
from ..bankcontroller.serializers import ShopServiceSerializer


class CurrentUserSerializer(serializers.ModelSerializer):

    balance = serializers.SerializerMethodField('get_balance')
    services = serializers.SerializerMethodField('shop_services')

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'first_name',
            'last_name',
            'phone',
            'balance',
            'services'
        )

    def get_balance(self, obj):
        wallet = Wallet.objects.get(user=obj)
        return wallet.balance

    def shop_services(self, obj):
        shops_services = obj.shops.all()
        return ShopServiceSerializer(shops_services, many=True).data


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email', 'id',
            'first_name', 'last_name',
        )


class UserCreateSerializer(serializers.ModelSerializer):

    phone = serializers.CharField(
        max_length=9,
        help_text='Последние цифры, 9 символов'
    )

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'phone',
            'password'
        )

    def validate_first_name(self, value):
        if value == '':
            raise serializers.ValidationError('Вас зовут ... ??')
        return value

    def validate_last_name(self, value):
        if value == '':
            raise serializers.ValidationError('Ваша фамилия ... ??')
        return value

    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError(
                "Последние цифры, 9 символов. И желательно цифры")
        if len(value) > 9:
            raise serializers.ValidationError(
                'Слишком длинный номер! Не кажется?')
        phone = f'+375{value}'
        if User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError(
                "Пользователь с таким номером телефона уже существует")
        return value

    def create(self, validated_data):
        phone = f"+375{validated_data['phone']}"
        user = User(
            email=validated_data['email'],
            last_name=validated_data['last_name'],
            first_name=validated_data['first_name'],
            phone=phone
        )
        user.set_password(validated_data['password'])
        user.save()
        wallet = Wallet.objects.create(user=user)
        wallet.save()
        return user
