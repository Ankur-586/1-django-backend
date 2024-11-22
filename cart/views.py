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
    queryset = Cart.objects.all()
    serializer_class = CartItemPostSerializer
    
    def partial_update(self, request, cart_id, variant_id):
        
        try:
            cart = Cart.objects.get(cart_id=cart_id)
        except Cart.DoesNotExist:
            return error_response('Cart with the provided ID does not exist.', status.HTTP_404_NOT_FOUND)
        
        if not variant_id:
            return error_response("Variant ID is required", status.HTTP_400_BAD_REQUEST)
        
        try:
            variant = ProductVariants.objects.get(id=variant_id)
        except ProductVariants.DoesNotExist:
            return error_response("Variant not found", status.HTTP_400_BAD_REQUEST)
        
        quantity = request.data.get('quantity') 
        
        serializer = self.serializer_class()
        try:
            cart_item = serializer.create_or_update_cart_item(cart, variant, quantity)
        except Exception as e:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': str(e),
                'data': []
            }, status=status.HTTP_400_BAD_REQUEST) 
        
        # If cart_item is None, it was deleted
        if cart_item == "Deleted":
            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Cart item removed successfully.',
                'data': []
            }, status=status.HTTP_200_OK)
        
        if cart_item == "NotFound":
            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Cart item not found.',
                'data': []
            }, status=status.HTTP_200_OK)

        serialized_data = self.serializer_class(cart_item)
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Quantity updated successfully',
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

'''    
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
            return error_response("Invalid format", status.HTTP_400_BAD_REQUEST)
        
        response_data = []
        errors = []

        # Validate each item
        for index, item_data in enumerate(items_data):
            if not isinstance(item_data, dict):
                errors.append(f"Item at index {index} must be a dictionary.")
                continue

            # Ensure each item has 'name' and 'quantity' fields
            if 'variant' not in item_data or 'quantity' not in item_data:
                errors.append(f"Item at index {index} must contain 'name' and 'quantity'.")
                continue

            # Check the validity of the 'name' field
            if not isinstance(item_data['name'], str) or len(item_data['name']) > 100:
                errors.append(f"Item at index {index} has an invalid 'name'.")
                continue

            # Check the validity of the 'quantity' field
            if not isinstance(item_data['quantity'], int) or item_data['quantity'] < 1:
                errors.append(f"Item at index {index} has an invalid 'quantity'.")
                continue

            # If validation passed, add to response_data
            response_data.append(item_data)


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

def get_serializer_context(self):
    context = super().get_serializer_context()
    context.update({"request": self.request})
    return context

Do not delete this. Needto ask chagpt this question.
def create_or_update_cart_item(self, cart, variant, quantity):
        """
        Logic to create or update a CartItem for a given cart and variant.
        If the quantity is 0, remove the cart item.
        """
        if quantity == 0:
            # Try to find the cart item and delete it
            try:
                cart_item = CartItem.objects.get(cart_id=cart, variant=variant)
                cart_item.delete()
                return "Deleted"  # Return None, indicating the item has been removed
            except CartItem.DoesNotExist:
                return "NotFound"  # If not found, return None as it was already removed

        # Otherwise, update or create the cart item
        cart_item, created = CartItem.objects.update_or_create(
            cart_id=cart,
            variant=variant,
            quantity=self.validate_quantity(quantity)
        )
        return cart_item this is my create method inside serializers and  class CartItemUpdateSet(viewsets.ViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartItemPostSerializer
    
    def partial_update(self, request, cart_id, variant_id):
        
        try:
            cart = Cart.objects.get(cart_id=cart_id)
        except Cart.DoesNotExist:
            return error_response('Cart with the provided ID does not exist.', status.HTTP_404_NOT_FOUND)
        
        if not variant_id:
            return error_response("Variant ID is required", status.HTTP_400_BAD_REQUEST)
        
        try:
            variant = ProductVariants.objects.get(id=variant_id)
        except ProductVariants.DoesNotExist:
            return error_response("Variant not found", status.HTTP_400_BAD_REQUEST)
        
        quantity = request.data.get('quantity') 
        
        serializer = self.serializer_class()
        try:
            cart_item = serializer.create_or_update_cart_item(cart, variant, quantity)
        except Exception as e:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': str(e),
                'data': []
            }, status=status.HTTP_400_BAD_REQUEST) 
        
        # If cart_item is None, it was deleted
        if cart_item == "Deleted":
            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Cart item removed successfully.',
                'data': []
            }, status=status.HTTP_200_OK)
        
        if cart_item == "NotFound":
            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Cart item not found.',
                'data': []
            }, status=status.HTTP_200_OK)

        serialized_data = self.serializer_class(cart_item)
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Quantity updated successfully',
            'data': serialized_data.data
        }, status=status.HTTP_200_OK) this is my view. My usrl http://127.0.0.1:8000/api/cart_update/cart_01RIEUPPWGMWIES/1/ and now when i update the quantiy inspite of updating the perticular bject it is creating new object 
'''