from django.db import models
import random, string, uuid
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from product.models import ProductVariants

User = get_user_model()

class Cart(models.Model):
    cart_id = models.CharField(max_length=20, primary_key=True, unique=True, editable=False) 
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.cart_id)
    
    class Meta:
        ordering = ['-created_at']
        
    def _generate_cart_id(self):
        """Generate a custom cart ID."""
        random_string = ''.join(random.choices((string.ascii_letters).upper() + string.digits, k=13))
        return f"cart_01{random_string}"

    def save(self, *args, **kwargs):
        """Override save method to generate custom cart_id if not provided."""
        if not self.cart_id:
            self.cart_id = self._generate_cart_id()
        super().save(*args, **kwargs)
    
class CartItem(models.Model):
    '''
    There is a issue in the cart_item_id creation function _generate_cart_item_id(self):. 
    See serializer's create method for more info.
    A doc string is added there as well
    '''
    cart_item_id = models.CharField(max_length=20, primary_key=True, unique=True, editable=False) 
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    variant = models.ForeignKey(ProductVariants, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.cart_item_id)
    
    def calculate_price(self):
        return self.quantity * self.price
    
    def _generate_cart_item_id(self):
        """Generate a custom cartItem ID."""
        # Prefix "item_01" followed by a random alphanumeric string of length 12
        random_string = ''.join(random.choices((string.ascii_letters).upper() + string.digits, k=13))
        return f"item_01{random_string}".strip()

    def save(self, *args, **kwargs):
        """Override save method to generate custom cart_item_id if not provided."""
        if not self.cart_item_id:
            self.cart_item_id = self._generate_cart_item_id()
        super().save(*args, **kwargs)
    
# how to test performance of django application

# i have a django-ecommerce project under development. i have many apps in this outof which i have a cart app
# and the models defined inside the cart app are below:
#     class Cart(models.Model):
#     cart_id = models.CharField(max_length=22, primary_key=True, unique=True, editable=False) 
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return str(self.cart_id)
    
#     class Meta:
#         ordering = ['-created_at']
        
#     def _generate_cart_id(self):
#         """Generate a custom cart ID."""
#         # Prefix "cart_01" followed by a random alphanumeric string of length 12
#         random_string = ''.join(random.choices((string.ascii_letters).upper() + string.digits, k=13))
#         return f"cart_01{random_string}"

#     def save(self, *args, **kwargs):
#         """Override save method to generate custom cart_id if not provided."""
#         if not self.cart_id:
#             self.cart_id = self._generate_cart_id()
#         super().save(*args, **kwargs)
    
# class CartItem(models.Model):
#     '''
#     There is a issue in the cart_item_id creation function _generate_cart_item_id(self):. 
#     See serializer's create method for more info.
#     A doc string is added there as well
#     '''
#     cart_item_id = models.CharField(max_length=22, primary_key=True, unique=True, editable=False) 
#     cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
#     variant = models.ForeignKey(ProductVariants, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
#     price = models.IntegerField(default = 0)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return str(self.cart_item_id)
    
#     def calculate_price(self):
#         return self.quantity * self.price
    
#     def _generate_cart_item_id(self):
#         """Generate a custom cartItem ID."""
#         # Prefix "item_01" followed by a random alphanumeric string of length 12
#         random_string = ''.join(random.choices((string.ascii_letters).upper() + string.digits, k=13))
#         return f"item_01{random_string}"

#     def save(self, *args, **kwargs):
#         """Override save method to generate custom cart_item_id if not provided."""
#         if not self.cart_item_id:
#             self.cart_item_id = self._generate_cart_item_id()
#         super().save(*args, **kwargs)
    
# Now, i also have a customeuser app in the project and  in this i have a customeuser model with different fields.
# And i was running a test cases using the test.py file present inside the customeuser app. 
# And i am getting a error while test is running: django.db.utils.DataError: value too long for type character varying(22)
# This error is assocated wit the cart app models. Beacuse if i dont use custom catr_id and cartitem_id and use uuid field inside 
# of this. then no issues

# My cart and cart_item models are empty na dhere is no data in the databadse