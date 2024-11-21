from django.contrib import admin

from .models import *
from .forms import OrderItemForm

class OrderItemInline(admin.TabularInline):
    form = OrderItemForm
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'cart_id', 'user_profile', 'order_date', 'status', 'total_amount', 'shipping_address')
    search_fields = ('order_id', 'order_date', 'status')
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'variant_id', 'quantity', 'price')
    search_fields = ('order_id',)

# Register other models if needed