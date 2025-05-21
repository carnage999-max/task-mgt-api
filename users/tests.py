import faker.factory
from rest_framework.test import APIClient, APITestCase
from .models import CustomUser
from rest_framework import status
from faker import Faker


class CustomUserTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(email="cod3.culture@gmail.com", password="123ezekiel")
        
    def test_create_user(self):
        fake = Faker()
        fake_email = fake.email()
        password = fake.password(length=10, special_chars=True, upper_case=True, digits=True)
    
        registration_data = {
            "email": str(fake_email),
            "password": str(password)
        }
        response = self.client.post('/api/v1/users/register/', data=registration_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    def test_login_user(self):
        login_data = {'email': "cod3.culture@gmail.com", "password": "123ezekiel"}
        response = self.client.post('/api/v1/users/login/', data=login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
