from rest_framework import viewsets
from rest_framework import viewsets, status
from rest_framework.response import Response

from cart.models import Cart, CartItem
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer # This is for view   
    
    def create(self, request, *args, **kwargs):
        cart_id = request.data.get('cart_id')
        try:
            cart = Cart.objects.get(pk=cart_id)
            cart_items = CartItem.objects.filter(cart_id=cart)
            if not cart_items.exists():
                return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
            
            order_data = request.data.copy()
            order_items_data = []
            for cart_item in cart_items:
                order_items_data.append({
                    'variant_id': cart_item.variant_id.id,
                    'quantity': cart_item.quantity,
                    'price': cart_item.variant_id.price
                })
            order_data['order_items'] = order_items_data
            order_serializer = self.get_serializer(data=order_data)
            order_serializer.is_valid(raise_exception=True)
            self.perform_create(order_serializer)
            headers = self.get_success_headers(order_serializer.data)
            return Response(order_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):
        serializer.save()