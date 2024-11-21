from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderItem

@receiver(post_save, sender=OrderItem)
def update_order_total(sender, instance, **kwargs):
    order = instance.order
    order.total_amount = sum(item.quantity * item.price for item in order.order_items.all())
    order.save()