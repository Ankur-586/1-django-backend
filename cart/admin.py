from django.contrib import admin
from .models import Cart, CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_per_page = 5
    list_display = ['cart_id', 'user', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['cart_id', 'user_id__username']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_per_page = 5
    list_display = ['cart_item_id', 'cart_id', 'variant', 'quantity']
    list_filter = ['cart_id', 'variant']
    search_fields = ['cart_item_id', 'cart_id__cart_id', 'variant__name']
    
    