from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

import uuid

from user_profile.models import UserProfile, User_Address
from product.models import ProductVariants
from cart.models import Cart

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'),
]

def create_order_id():
    static_part = 'ord_'
    last_order = Order.objects.all().order_by('id').last()
    if not last_order:
        new_order_number = 1
    else:
        last_order_number = int(last_order.order_id[len(static_part):])
        new_order_number = last_order_number + uuid
    order_id = f"{static_part}{new_order_number:02d}"
    return order_id

class Order(models.Model):
    order_id = models.CharField(max_length=12, unique=True, blank=True)
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10,default='Pending', choices=STATUS_CHOICES)
    total_amount = models.FloatField()
    shipping_address = models.ForeignKey(User_Address, on_delete=models.CASCADE)
    
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = create_order_id()
        super(Order, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.order_id
        
class OrderItem(models.Model):
    order_id = models.ForeignKey(Order,on_delete=models.CASCADE, related_name='order_items')
    variant_id = models.ForeignKey(ProductVariants, on_delete=models.CASCADE, related_name='variants_items')
    quantity = models.IntegerField(default=1)
    price = models.FloatField()
    
    # def clean(self):
    #     super().clean()
    #     product = self.variant_id.product
    #     min_quantity = product.minimum_order_quantity
    #     max_quantity = product.maximum_order_quantity

    #     if not (min_quantity <= self.quantity <= max_quantity):
    #         raise ValidationError(f"Quantity must be between {min_quantity} and {max_quantity}.")
    
    # def save(self, *args, **kwargs):
    #     if not self.price:
    #         self.price = self.variant_id.price 
    #     super(OrderItem, self).save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_id.order_id} - {self.variant_id.variant_name} x {self.quantity}"
