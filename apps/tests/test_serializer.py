import decimal

from apps.bankcontroller.models import Service, ShopService, Wallet
from apps.bankcontroller.serializers import (CreateMoneyCardSerializer,
                                             ServiceSerializer)
from apps.users.models import User
from apps.users.serializers import (CurrentUserSerializer,
                                    UserCreateSerializer, UserListSerializer)
from faker import Faker as FakerBase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

faker = FakerBase()


class TestApiSerializer(APITestCase):

    def setUp(self):
        self.service = Service.objects.create(
            name='test1',
            description='test1',
            price=decimal.Decimal(1200.00),
            currency='BYN'
        )
        Service.objects.create(
            name='test2',
            description='test2',
            price=decimal.Decimal(1300.00),
            currency='BYN'
        )
        Service.objects.create(
            name='test3',
            description='test3',
            price=decimal.Decimal(1400.00),
            currency='BYN'
        )
        Service.objects.create(
            name='test4',
            description='test4',
            price=decimal.Decimal(1500.00),
            currency='BYN'
        )
        self.admin = User.objects.create(
            email=faker.email(),
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            phone='123456789',
            is_staff=True,
            is_superuser=True
        )
        self.valid_user = User.objects.create(
            email=faker.email(),
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            phone='123456780',
            is_staff=True,
            is_superuser=True
        )
        self.token = Token.objects.create(
            user=self.valid_user
        )
        self.api_authentication()

        self.wallet = Wallet.objects.create(
            number_walet="101010",
            balance=decimal.Decimal(1000),
            user=self.admin
        )
        self.shop_service = ShopService.objects.create(
            user=self.admin,
            service=self.service,
        )

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + str(self.token))

    def test_get_all_service(self):
        response = self.client.get('/services/')
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Service.objects.count(), 4)
        self.assertEqual(response.data['results'], serializer.data)

    def test_get_service(self):
        response = self.client.get('/services/1/')
        services = Service.objects.get(id=1)
        serializer = ServiceSerializer(services)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.data['name'], serializer.data['name'])
        self.assertEqual(response.data['description'],
                         serializer.data['description'])
        self.assertEqual(response.data['price'], serializer.data['price'])
        self.assertEqual(response.data['currency'],
                         serializer.data['currency'])

    def test_get_shop_service(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/services/1/shop/')
        services = Service.objects.get(id=1)
        serializer = ServiceSerializer(services)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data['purchased'], False)
        self.client.force_authenticate(user=None)
        self.assertEqual(serializer.data['purchased'], False)

    def test_create_money_card(self):
        data = {
            "number": "1111222233334444",
            "month": "12",
            "year": "2021",
            "amount": 1000
        }
        self.client.force_authenticate(user=None)
        response = self.client.post("/create_money_card/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(user=self.admin)
        response = self.client.post("/create_money_card/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_users_list(self):
        response = self.client.get('/users/')
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)

    def test_get_user(self):
        response = self.client.get('/users/1/')
        user = User.objects.get(id=1)
        serializer = UserListSerializer(user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_user_serializer(self):
        data = {
            "email": faker.email(),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            'phone': '123456789',
            "password": faker.password()
        }
        serializer = UserCreateSerializer(data)
        response = self.client.post("/users/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], serializer.data['email'])

    def test_current_user(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get('/users/me/')
        user = User.objects.get(id=1)
        serializer = CurrentUserSerializer(user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone'], serializer.data['phone'])
        self.assertEqual(serializer.data['balance'], '1000.00 BYN')

    def test_bankcontroller_serializer_error(self):
        data = {
            "number": "123",
            "month": "12",
            "year": "2021",
            "amount": 1000
        }
        serializer = CreateMoneyCardSerializer(data=data)
        message_error = 'Номер карточки не может быть менее 16 символов'
        assert not serializer.is_valid()
        assert serializer.validated_data == {}
        assert serializer.errors == {'number': [message_error]}

    def test_users_serializer_errors(self):
        serializer = UserCreateSerializer(data={})
        message_error = [
            'Вас зовут apps.. ??',
            'Ваша фамилия apps.. ??',
            'Обязательное поле.',
            'Слишком длинный номер! Не кажется?',
            'Слишком короткий номер! Не кажется?',
            "Пользователь с таким номером телефона уже существует",
            'Убедитесь, что это значение содержит не более 9 символов.',
            "Последние цифры, 9 символов. И желательно цифры",
        ]
        assert not serializer.is_valid()
        assert serializer.validated_data == {}
        assert serializer.errors['email'][0] == message_error[2]
        assert serializer.errors['phone'][0] == message_error[2]
        assert serializer.errors['password'][0] == message_error[2]
        serializer = UserCreateSerializer(
            data={
                'first_name': '',
                'last_name': ''
            }
        )
        assert not serializer.is_valid()
        assert serializer.errors['first_name'][0] == message_error[0]
        assert serializer.errors['last_name'][0] == message_error[1]
        serializer = UserCreateSerializer(data={'phone': 'awdaw'})
        assert not serializer.is_valid()
        assert serializer.errors['phone'][0] == message_error[-1]
        serializer = UserCreateSerializer(data={'phone': '123'})
        assert not serializer.is_valid()
        assert serializer.errors['phone'][0] == message_error[4]
        serializer = UserCreateSerializer(data={'phone': '1234567890'})
        assert not serializer.is_valid()
        assert serializer.errors['phone'][0] == message_error[-2]

    def test_shop_service(self):
        self.client.force_authenticate(user=None)
        request = self.client.get('/services/1/shop/')
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(user=self.admin)
        request = self.client.get('/services/1/shop/')
        self.assertEqual(request.status_code, status.HTTP_200_OK)
