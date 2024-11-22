from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Role, CustomUser

User = get_user_model()

# class CustomUserModelTest(TestCase):
#     def test_superuser_creation(self):
#         email = "test@gmail.com"
#         username = "test123"
#         password = "intex123"
        
#         user = CustomUser.objects.create_superuser(email=email, username=username, password=password)
#         self.assertEqual(user.email, email)
#         self.assertEqual(user.username, username)
#         self.assertTrue(user.is_superuser)
#         self.assertTrue(user.is_staff)
#         self.assertTrue(user.is_active)
#         self.assertTrue(user.check_password(password))
    
#     def test_user_creation(self):
#         email = "test@gmail.com"
#         username = "test123"
#         password = "intex123"
        
#         user = CustomUser.objects.create_user(email=email, username=username, password=password)
#         self.assertEqual(user.email, email)
#         self.assertEqual(user.username, username)
#         self.assertFalse(user.is_superuser) # checks if the value of user.is_superuser is False : If user.is_superuser is False, the test will pass.
#         self.assertFalse(user.is_staff)
#         self.assertTrue(user.is_active)
#         self.assertTrue(user.check_password(password))
    
#     def test_full_name_propertry(self):
#         first_name = '454654'
#         last_name = 'Singh'
#         user = CustomUser(first_name=first_name, last_name=last_name)
#         self.assertEqual(user.full_name, f"{first_name} {last_name}")