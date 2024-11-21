from rest_framework import serializers
from django.utils import timezone
import logging

from .models import Order, OrderItem
from product.models import ProductVariants
# from cart.serializers import CartSerializer

logger = logging.getLogger('user_profiles')

class OrderItemSerializer(serializers.ModelSerializer):
    '''
    PrimaryKeyRelatedField allows the use of primary key for the related model
    '''
    variant_id = serializers.PrimaryKeyRelatedField(queryset=ProductVariants.objects.all())
    
    '''
    Making the price field optional as it can be derived from the variant
    '''
    price = serializers.FloatField(required=False)

    class Meta:
        model = OrderItem
        fields = ['variant_id', 'quantity', 'price']

    def get_price(self, obj):
        """
        This method ensures that the price is dynamically fetched based on the variant.
        """
        if hasattr(obj, 'variant_id'):
            return obj.variant.price
        return 0

    def validate_variant_id(self, value):
        """
        This method ensures that the variant_id is valid by checking its existence.
        """
        if not ProductVariants.objects.filter(pk=value.id).exists():
            raise serializers.ValidationError("Invalid variant ID")
        return value

    def validate(self, data):
        """
        This method ensures that the price is set, either from the data or from the ProductVariants.
        """
        variant = data.get('variant_id')
        quantity = data.get('quantity')
        if not quantity:
            raise serializers.ValidationError("Quantity is required.")
        
        # Ensure quantity is within allowed range
        product = variant.product
        if not (product.minimum_order_quantity <= quantity <= product.maximum_order_quantity):
            raise serializers.ValidationError(f"Quantity must be between {product.minimum_order_quantity} and {product.maximum_order_quantity}.")
        
        # Ensure price is set, either from the data or from the variant
        if not data.get('price'):
            data['price'] = variant.price
        elif data['price'] != variant.price:
            raise serializers.ValidationError("Price provided does not match the variant price.")

        return data

class OrderSerializer(serializers.ModelSerializer):
    # Nested serializer to handle multiple order items
    order_items = OrderItemSerializer(many=True)
    
    # Custom serializer method field to format order_date
    order_date = serializers.SerializerMethodField()
    
    # Making the total_amount field optional to calculate it later
    total_amount = serializers.FloatField(required=False)

    class Meta:
        model = Order
        fields = ['order_id', 'cart_id', 'user_profile', 'order_date', 'status', 'total_amount', 'shipping_address', 'order_items']

    def get_order_date(self, obj):
        """
        This function converts timestamp in ISO 8601 format to a properly formatted datetime string.
        """
        if obj.order_date:
            local_time = timezone.localtime(obj.order_date)
            return local_time.strftime('%Y-%m-%d %H:%M:%S')
        return 'None'

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items', [])
        total_amount = 0
        for item_data in order_items_data:
            item_data['price'] = item_data.get('price', item_data['variant_id'].price)
            total_amount += item_data['price'] * item_data['quantity']
        validated_data['total_amount'] = total_amount
        order = Order.objects.create(**validated_data)
        for item_data in order_items_data:
            OrderItem.objects.create(order_id=order, **item_data)
        return order

    # def update(self, instance, validated_data):
    #     order_items_data = validated_data.pop('order_items')
    #     instance.status = validated_data.get('status', instance.status)
    #     instance.total_amount = validated_data.get('total_amount', instance.total_amount)
    #     instance.shipping_address = validated_data.get('shipping_address', instance.shipping_address)
    #     instance.save()
    #     # Update or create order items
    #     instance.order_items.all().delete()
    #     for item_data in order_items_data:
    #         OrderItem.objects.create(order_id=instance, **item_data)
    #     return instance

