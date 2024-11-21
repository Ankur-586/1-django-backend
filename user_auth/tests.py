from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Role, CustomUser

User = get_user_model()

class CustomUserModelTest(TestCase):
    def test_user_creation(self):
        email = "test@gmail.com"
        username = "test123"
        password = "intex123"
        
        user = CustomUser.objects.create(email=email, username=username, password=password)
        self.assertEqual(user.email, email)
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))