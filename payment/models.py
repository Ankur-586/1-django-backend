from django.db import models
import uuid

from order.models import Order

class Payment(models.Model):
    payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    # payment_method = models.CharField()