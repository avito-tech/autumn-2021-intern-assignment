from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

faker_suer = Faker()


class RegistrationTest(APITestCase):
    """Регистрация пользователя"""

    def test_registration(self):
        data = {
            "email": faker_suer.email(),
            "first_name": faker_suer.first_name(),
            "last_name": faker_suer.last_name(),
            'phone': '123456789',
            "password": faker_suer.password()
        }
        response = self.client.post("/users/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    
