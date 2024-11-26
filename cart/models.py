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
    variant = models.ForeignKey(ProductVariants, on_delete=models.CASCADE, related_name='product_variant')
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.cart_item_id)
    
    # class Meta:
    #     unique_together = ('cart_id', 'cart_item_id') 

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
'''
def _generate_cart_item_id(self):
    """Generate a custom cartItem ID using UUID."""
    return f"item_01{uuid.uuid4().hex[:13]}"  # Get the first 13 characters of the UUID hex
'''