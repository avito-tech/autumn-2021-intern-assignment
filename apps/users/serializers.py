from rest_framework import serializers
from .models import User


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email', 'id',
            'first_name', 'last_name',
            'phone'
        )


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email', 'id',
            'username',
            'first_name',
            'last_name',
            'phone',
            'password'
        )

    def validate_first_name(self, value):
        if value == '':
            raise serializers.ValidationError('Вас зовут ... ??')

    def validate_last_name(self, value):
        if value == '':
            raise serializers.ValidationError('Ваша фамилия ... ??')

    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError(
                "Формат ввода: +375... и желательно цифры")
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
        return user
