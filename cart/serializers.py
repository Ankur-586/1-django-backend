from rest_framework import serializers,status
from rest_framework.response import Response

from .models import Cart, CartItem
from product.models import ProductVariants
from core.utils import CustomValidation

from django.utils import timezone

class CartItemSerializer(serializers.ModelSerializer):
    '''
    -> This serializer is being used in the CartSerializer Below and is only for read only

    -> SerializerMethodField is read only
    '''
    variant = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['variant']
    
    def get_variant(self, obj):
        '''
        obj : cart_item_id
        '''
        product_variant = obj.variant
        variant_name = product_variant.variant_name
        thumbnail = product_variant.images.first().image.url if product_variant.images.exists() else None
        price = product_variant.price
        quantity = obj.quantity
        item_total = obj.calculate_price()
        product = {
            'id': obj.variant.product.id,
            'product_name': obj.variant.product.product_name,
            'product_image': product_variant.product.thumbnail.url if product_variant.product.thumbnail.url else None
        }
        return {
            'id': product_variant.pk,
            'variant_title': variant_name,
            'thumbnail': thumbnail,
            'item_price': price,
            'quantity':quantity,
            'item_total':item_total,
            'product': product
        }

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True)
    user = serializers.SerializerMethodField()
    timestamps = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['cart_id','timestamps', 'user','cart_items']
    
    def get_timestamps(self, obj):
        # print(dir(obj))
        """
        This function converts created_at and updated_at timestamps to properly formatted datetime strings.
        """
        timestamps = {}
        
        if obj.created_at:
            local_created_time = timezone.localtime(obj.created_at)
            timestamps['created_at'] = local_created_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            timestamps['created_at'] = None

        if obj.updated_at:
            local_updated_time = timezone.localtime(obj.updated_at)
            timestamps['updated_at'] = local_updated_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            timestamps['updated_at'] = None

        return timestamps
    
    def get_user(self, obj):
        user_info = obj.user
        if user_info:
          return {
            'id': user_info.id,
            'user_name': user_info.username,
          }
        return None

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
        return cart_item
    
    def get_response_data(self, cart, cart_items, user):
        items_data = []
        for cart_item in cart_items:
            items_data.append({
                "variant": {
                    "variant_id": cart_item.variant.pk,
                    "variant_name": cart_item.variant.variant_name,
                    "variant_image": cart_item.variant.images.first().image.url if cart_item.variant.images.exists() else None,
                    # "product": {
                    #     "category": cart_item.variant.product.category.category_name,
                    #     "name": cart_item.variant.product.product_name,
                    # }
                },
                "quantity": cart_item.quantity,
                "price": cart_item.price,
                "total_price": cart_item.calculate_price(),
            })
        return {
            'cart_id': cart.cart_id,
            "created_at": cart.created_at,
            "updated_at": cart.updated_at,
            "user": user.username if user else None,
            "items": items_data
        }
    
'''
if quantity == 0:
            # Try to find the cart item and delete it
            try:
                cart_item = CartItem.objects.get(cart_id=cart, variant=variant)
                cart_item.delete()
                return Response({
                    'status': status.HTTP_200_OK,
                    'message': 'Cart item removed successfully.',
                }, status=status.HTTP_200_OK)
            except CartItem.DoesNotExist:
                return Response({
                    'status': status.HTTP_404_NOT_FOUND,
                    'message': 'Cart item not found.',
                }, status=status.HTTP_404_NOT_FOUND)

items_data = self.context["request"].data.get('items', [])
    # Collect all variant IDs from the items
    variant_ids = {item.get('variant') for item in items_data if item.get('variant') is not None}
    # Fetch existing variants in a single query
    existing_variants = set(ProductVariants.objects.filter(pk__in=variant_ids).values_list('pk', flat=True))
    # Identify non-existing variants
    non_existing_variants = variant_ids - existing_variants
    if non_existing_variants:
        # Use a single error message for one or multiple non-existing IDs
        variant_ids_str = ', '.join(map(str, non_existing_variants))
        raise CustomValidation(
            f"No product_variant(s) with the given ID(s): {variant_ids_str} were found",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    return super().to_internal_value(data)

def to_internal_value(self, data):
    variant_id = data.get('variant')
    print(variant_id)
    if not ProductVariants.objects.filter(pk=variant_id).exists():
        raise CustomValidation("No product with the given id was found", status_code=status.HTTP_400_BAD_REQUEST)
    return super().to_internal_value(data)

def create(self, validated_data):
        request = self.context['request']
        user = request.user if request.user.is_authenticated else None
        print(user)
        if user is None:
            session = request.session
            cart_id = session.get('cart_id', None)
            if cart_id:
                cart = Cart.objects.get(cart_id=cart_id)
            else:
                cart = Cart.objects.create()
                session['cart_id'] = str(cart.cart_id)
        else:
            cart, created = Cart.objects.get_or_create(user=user)
            
        cart_items = []
        variant = validated_data.pop('variant_id')  # Retrieve and remove variant_id from item_data

        validated_data['cart_id'] = cart
        validated_data['variant'] = variant
        validated_data['price'] = validated_data.get('price', variant.price)
        
        cart_item = CartItem(**validated_data)
        cart_items.append(cart_item)

        CartItem.objects.bulk_create(cart_items)
        
        # Prepare the response data
        response_data = [{
            "cart_id": cart.cart_id,
            "variant_id": cart_item.variant.pk,
            "variant_name": cart_item.variant.variant_name,
            "variant_image": cart_item.variant.images.first().image.url if cart_item.variant.images.exists() else None, # i have used related_name property
            "quantity": cart_item.quantity,
            "price": cart_item.price,
            "total_price": cart_item.calculate_price()
        } for cart_item in cart_items]

        return response_data
'''
# '''
# cart functionality in drf without using session: 
# case 1: if cart is created when there is no user associated with it.
# case 2: if cart is created and then later bind a user to that perticular cart
# ------------------------------------------------------

# i dont have region id in my db. i will add later. but for future
# please make some provision that i can add it later