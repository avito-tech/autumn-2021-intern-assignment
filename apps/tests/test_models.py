import decimal

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from faker import Faker as FakerBase

from ..bankcontroller.models import MoneyCard, Service, ShopService, Wallet
from ..users.models import User

faker = FakerBase()


class CreateModels(TestCase):

    def setUp(self):
        self.guest_client = Client()
        self.user = get_user_model().objects.create_user(
            email='test@test.test',
            first_name='Test',
            last_name='Testovich',
            password="Test1Test"
        )
        self.service = Service.objects.create(
            name='test',
            description='test',
            price=decimal.Decimal(1200.00),
            currency='BYN'
        )

    def test_return_user(self):
        first_name, last_name = faker.first_name(), faker.last_name()
        full_name = User.objects.create(
            first_name=first_name,
            last_name=last_name,
        )
        self.assertEqual(str(full_name), full_name.get_full_name())

    def test_return_wallet(self):
        wallet = Wallet.objects.create(
            number_walet='122321',
            balance=decimal.Decimal(1200.00),
            user=self.user
        )
        self.assertEqual(str(wallet), "Test Testovich - 122321")

    def test_return_service(self):
        service = Service.objects.create(
            name='test',
            description='test',
            price=decimal.Decimal(1200.00),
            currency='BYN'
        )
        self.assertEqual(str(service), service.name)

    def test_return_money_card(self):
        money_card = MoneyCard.objects.create(
            number="0000111122223333",
            year="2021",
            month='11',
            amount=decimal.Decimal(1200.00),
            user=self.user
        )
        res = (
            f'Зачисление №{money_card.id} на сумму: {money_card.amount}. '
            f'Пользователем: {money_card.user}'
        )
        self.assertEqual(str(money_card), res)

    def test_return_shop_service(self):
        shop_service = ShopService.objects.create(
            service=self.service,
            user=self.user
        )
        res = (
            f"{shop_service.user} купил услугу {shop_service.service.name} "
            f"за {shop_service.service.price}"
        )
        self.assertEqual(str(shop_service), res)

