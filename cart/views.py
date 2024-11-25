from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError

from core.utils import error_response
from .models import Cart, CartItem
from product.models import ProductVariants
from .serializers import CartSerializer, CartItemPostSerializer

# implemet a feature where i enter a wrong cart id then i get a proprt message not a bad html
class CartViewSet(generics.RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer 
    lookup_field = 'cart_id'
    http_method_names = ['get']
    
    def retrieve(self, request, *args, **kwargs):
        try:
            # Get the object based on the primary key provided in the URL
            instance = self.get_object()
            serializer = self.get_serializer(instance) 
            payload = {
                "status": status.HTTP_200_OK,
                "message": 'Cart Detail',
                "data": serializer.data
            }
            return Response(payload, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": str(e),
                "data": []
            }, status=status.HTTP_400_BAD_REQUEST)

class CartItemPostSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    queryset = CartItem.objects.all()
    serializer_class = CartItemPostSerializer 
    permission_classes = [AllowAny]
    http_method_names = ['post']
    
    def create(self, request, *args, **kwargs):
        user = request.user if request.user.is_authenticated else None
        cart_id = self.kwargs.get('cart_id')
        items_data = request.data.get('items', [])

        if not isinstance(items_data, list):
            return error_response("'items' must be a list", status.HTTP_400_BAD_REQUEST)
        
        if not items_data:
            return error_response("items expects a list with data in dictionary format", status.HTTP_400_BAD_REQUEST)
        
        response_data = []
        errors = []

        # Validate each item
        for item_data in items_data:
            item_serializer = self.get_serializer(data=item_data)
            if not item_serializer.is_valid():
                errors.extend([
                    f"{field}: {message}"
                    for field, messages in item_serializer.errors.items()
                    for message in messages
                ])
            else:
                response_data.append(item_serializer.validated_data)

        if errors:
            # If there are validation errors, return a 400 response with the error details
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': "Validation failed",
                'errors': errors
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Now create the Cart and CartItems if validation passed
            cart = self.get_serializer().create(response_data, user, cart_id)
        except Exception as e:
            # In case of any unexpected error, return a 400 response with the error message
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': f"Error creating cart items: {str(e)}",
                'data': []
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Retrieve the created cart items
        cart_items = CartItem.objects.filter(cart_id=cart.cart_id)
        response_data_final = self.get_serializer().get_response_data(cart, cart_items, user)

        return Response({
            'status': status.HTTP_201_CREATED,
            'message': 'Items added to cart successfully.',
            'cart': response_data_final
        }, status=status.HTTP_201_CREATED)

class CartItemUpdateSet(viewsets.ViewSet):
    '''
    This view update the quantiy of variant
    and if quantity = 0 is posted then then 
    it removes the variant from cart_item
    '''
    queryset = CartItem.objects.all()
    serializer_class = CartItemPostSerializer
    
    def partial_update(self, request, cart_id, cart_item_id):
        
        try:
            cart = Cart.objects.get(cart_id=cart_id)
        except Cart.DoesNotExist:
            return error_response('Cart with the provided ID does not exist.', status.HTTP_404_NOT_FOUND)
        
        if not cart_item_id:
            return error_response("CartItem ID is required", status.HTTP_400_BAD_REQUEST)
        
        try:
            cart_item = CartItem.objects.get(cart_item_id=cart_item_id)
        except CartItem.DoesNotExist:
            return error_response("CartItem not found", status.HTTP_400_BAD_REQUEST)
        
        quantity = request.data.get('quantity') 
        
        serializer = self.serializer_class()
        try:
            cart_items = serializer.update_cart_item(cart, cart_item, quantity)
        except Exception as e:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': str(e),
                'data': []
            }, status=status.HTTP_400_BAD_REQUEST) 
        
        # If cart_item is None, it was deleted
        if cart_items == "Deleted":
            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Cart item removed successfully.',
                'data': []
            }, status=status.HTTP_200_OK)
        
        if cart_items == "NotFound":
            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Cart item not found.',
                'data': []
            }, status=status.HTTP_200_OK)

        serialized_data = self.serializer_class(cart_items)
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Quantity updated successfully',
            'data': serialized_data.data
        }, status=status.HTTP_200_OK)
                
class CartItemUpdateExistingItemSet(viewsets.ViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemPostSerializer

    def create(self, request, cart_id):
        try:
            cart = Cart.objects.get(cart_id=cart_id)
        except Cart.DoesNotExist:
            return error_response('Cart with the provided ID does not exist.', status.HTTP_404_NOT_FOUND)
        
        variant = request.data.get('variant_id')
        quantity = request.data.get('quantity')

        serializer = self.serializer_class()
        
        try:
            cart_id = serializer.add_item_to_cart(cart, variant, quantity)
        except Exception as e:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': str(e),
                'data': []
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serialized_data = self.serializer_class(cart_id)
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Item added to Cart Items',
            'data': serialized_data.data
        }, status=status.HTTP_200_OK)

class AssociateUserWithCart(viewsets.ModelViewSet):
    '''
    This view binds the user to a particular cart id 
    When the cart id is created without a user.
    '''
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    lookup_field = 'cart_id'

    def perform_create(self, serializer):
        # Automatically associate the cart with the authenticated user
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        # Fetch the cart object
        cart = self.get_object()

        # Only allow updating the user if the cart is not already linked to a user
        if cart.user and cart.user != request.user:
            return Response(
                {
                'status': status.HTTP_403_FORBIDDEN,
                'message': "This cart is already associated with another user.",
                'data': []
                }, status=status.HTTP_403_FORBIDDEN)

        # Associate the cart with the authenticated user
        cart.user = request.user
        cart.save()

        serializer = self.get_serializer(cart)
        
        response = {
            'status': status.HTTP_200_OK,
            'messgae': 'User Binded with cart',
            'data': serializer.data 
        }
        return Response(response, status=status.HTTP_200_OK)
