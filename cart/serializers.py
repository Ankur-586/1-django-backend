from rest_framework import serializers,status
from rest_framework.response import Response

from .models import Cart, CartItem
from product.models import ProductVariants
from core.utils import CustomValidation

from django.utils import timezone

class CartSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    timestamps = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['cart_id','timestamps', 'user']

class CartItemPostSerializer(serializers.ModelSerializer):
    '''
    PrimaryKeyRelatedField allows you to write the primary key of the ProductVariants when creating or updating a CartItem
    '''
    variant = serializers.PrimaryKeyRelatedField(queryset=ProductVariants.objects.all(), write_only=True)
    quantity = serializers.IntegerField(default=1)
    
    class Meta:
        model = CartItem
        fields = ['variant', 'quantity']
    
    def validate_quantity(self, value):
        if value is None:
            raise CustomValidation("Quantity is required", status_code=status.HTTP_400_BAD_REQUEST)
        if value < 1:
            raise CustomValidation("Quantity must be at least 1.", status_code=status.HTTP_400_BAD_REQUEST)
        elif value > 5:
            raise CustomValidation("Quantity can't be at more than 5", status_code=status.HTTP_400_BAD_REQUEST)
        return value
    
    def validate_variant(self, value):
        variant = ProductVariants.objects.get(pk=value.pk)
        if not variant.is_active:
            raise CustomValidation("The selected variant is out of stock!!", status_code=status.HTTP_400_BAD_REQUEST)
        return value
    
    def to_internal_value(self, data):
        items_data = self.context["request"].data.get('items') 
        non_existing_variants = []
        for item in items_data:
            variant_id = item.get('variant')
            if not ProductVariants.objects.filter(pk=variant_id).exists():
                non_existing_variants.append(variant_id)
        if non_existing_variants:
            if len(non_existing_variants) > 1:
                raise CustomValidation(f"No product_variant with the given ID's {non_existing_variants} was found", 
                                       status_code=status.HTTP_400_BAD_REQUEST)
            raise CustomValidation(f"No product_variant with the given ID {non_existing_variants} was found", 
                                   status_code=status.HTTP_400_BAD_REQUEST)
        return super().to_internal_value(data) 
    
    def create(self, validated_data, user, cart_id):
        '''
        This is my post Response
        '''
        cart, created = Cart.objects.get_or_create(user=user, cart_id=cart_id)

        cart_items = []
        for item_data in validated_data:
            variant = item_data.pop('variant')
            quantity = item_data['quantity']
            cart_item = CartItem(
                cart_id=cart,
                variant=variant,
                quantity=self.validate_quantity(quantity),
                price=variant.price
            )
            '''
            Note: A doc string has been added in the model. Refer there to understand the issue.
            When using bulk_create(), you are bypassing the save() method, which generates the cart_item_id. 
            Therefore, you need to ensure that the cart_item_id is manually set, as done above.
            '''
            cart_item.cart_item_id = cart_item._generate_cart_item_id()
            cart_items.append(cart_item)
        # Bulk create cart items
        CartItem.objects.bulk_create(cart_items)
        return cart

    def update_cart_item(self, cart, cart_item_id, quantity):
        """
        Logic to update a CartItem for a given cart and cart_item.
        If the quantity is 0, remove the cart item.
        
        if quantity is being deleted like -1. Then observer.
        """
        
        if quantity == 0:
            # Try to find the cart item and delete it
            try:
                cart_items = CartItem.objects.get(cart_id=cart, cart_item_id=cart_item_id)
                cart_items.delete()
                return "Deleted"  # Return None, indicating the item has been removed
            except CartItem.DoesNotExist:
                return "NotFound"  # If not found, return None as it was already removed
        
        # Get the existing CartItem
        cart_item_instance = CartItem.objects.get(cart_id=cart, cart_item_id=cart_item_id)

        MAX_QUANTITY = cart_item_instance.variant.product.maximum_order_quantity

        # Calculate the new quantity (add the incoming quantity to the existing one)
        new_quantity = cart_item_instance.quantity + quantity

        # Check if the new quantity exceeds the maximum allowed
        if new_quantity > MAX_QUANTITY:
            raise CustomValidation("Total quantity can't exceed 5.", status_code=status.HTTP_400_BAD_REQUEST)

        # Update the quantity and save the CartItem
        cart_item_instance.quantity = new_quantity
        cart_item_instance.save()  # Save the updated CartItem instance

        return CartItem.objects.filter(cart_id=cart)
    
    def add_item_to_cart(self, cart, variant, quantity):
        print('from serilaizers',variant)
        # Try to get the ProductVariant instance
        try:
            product_variant = ProductVariants.objects.get(id=variant)
        except ProductVariants.DoesNotExist:
            raise ValueError("Product variant does not exist in theh database.")

        # Check if the CartItem for this variant already exists in the given cart
        cart_item = CartItem.objects.filter(cart_id=cart, variant=variant).first()
        MAX_QUANTITY = cart_item.variant.product.maximum_order_quantity
        
        if not cart_item:
            print('first_part')
            # If CartItem already exists, update the quantity
            cart_item.quantity += quantity
            if cart_item.quantity > MAX_QUANTITY:
                raise CustomValidation("Total quantity can't exceed 5.", status_code=status.HTTP_400_BAD_REQUEST)
            
            cart_item.save()
            return cart_item
        else:
            print('second part')
            # If CartItem doesn't exist, create a new CartItem
            cart_item = CartItem.objects.create(
                cart_id=cart,
                variant=product_variant,
                quantity=quantity,
                price = product_variant.price
            )
        cart_item.price = cart_item.calculate_price()  # Add this line if you need to save the total price in the model
        cart_item.save()

        return cart_item
'''
NOTE: In the response. when i am updating a object it going up and down. 

------------
Do Not Delete:
--------------
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

        # Now, check if the CartItem exists manually
        try:
            cart_item = CartItem.objects.get(cart_id=cart, variant=variant)
            # If found, update the quantity and price
            cart_item.quantity = self.validate_quantity(quantity)
            cart_item.price = variant.price
            cart_item.save()  # Update the existing record
            return cart_item
        except CartItem.DoesNotExist:
            # If the CartItem doesn't exist, create a new one
            cart_item = CartItem(
                cart_id=cart,
                variant=variant,
                quantity=self.validate_quantity(quantity),
                price=variant.price
            )
            cart_item.cart_item_id = cart_item._generate_cart_item_id()  # Generate the ID
            cart_item.save()  # Save the new record
            return cart_item
'''
# ------------------------------------------------------

# i dont have region id in my db. i will add later. but for future
# please make some provision that i can add it later