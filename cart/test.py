from django.test import TestCase
from .models import Cart
from user_auth.models import CustomUser

class Custome_cart_creation(TestCase):
    def test_cart_creation_without_user(self):
        cart = Cart.objects.create(user=None)
        print('from 1st fun', cart)
        
    def test_cart_creation_with_user(self):
        # user = CustomUser.objects.create(email='test@gmail.com', username='test',first_name='test',last_name='test',password='test')
        user = CustomUser.objects.first()
        cart = Cart.objects.create(user=user)
        print('from 2nd fun',cart)    
    