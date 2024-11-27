from django.utils import timezone
from django.db.models import Prefetch

from product.models import ProductVariants
from .serializers import CartSerializer  

def get_cart_response_data(cart, cart_items, user):
    """
    A helper function to format the cart response in the required structure.
    Optimized for performance.
    """
    # Prefetch related data to avoid repeated queries
    variants = Prefetch('variant', queryset=ProductVariants.objects.select_related(
        'product').prefetch_related('images').all())
    
    cart_items = cart_items.prefetch_related(variants)
    
    items_data = []
    for cart_item in cart_items:
        variant = cart_item.variant
        product = variant.product
        
        # Calculate item total in memory and avoid repeated function calls
        item_total = cart_item.calculate_price()

        items_data.append({
            "cart_item_id": cart_item.cart_item_id,
            'timestamps': get_timestamps(cart_item),
            "variant": {
                "variant_id": variant.pk,
                "variant_title": variant.variant_name,
                "variant_images": variant.images.first().image.url if variant.images.exists() else None,
                "item_price": cart_item.price,
                "product": {
                    "id": product.id,
                    "product_name": product.product_name,
                    "product_image": product.thumbnail.url if product.thumbnail else None
                }
            },
            "subtotal_amount": {
                "quantity": cart_item.quantity,
                "item_total": item_total,
            }
        })

    return {
        'cart_id': cart.cart_id,
        'timestamps': get_timestamps(cart),
        'user': get_user(cart),
        'cart_items': items_data
    }

def get_timestamps(time_stamp):
    """
    Helper function to format the timestamps.
    """
    timestamps = {}

    if time_stamp.created_at:
        local_created_time = timezone.localtime(time_stamp.created_at)
        timestamps['created_at'] = local_created_time.strftime('%Y-%m-%d %H:%M:%S')
    else:
        timestamps['created_at'] = None

    if time_stamp.updated_at:
        local_updated_time = timezone.localtime(time_stamp.updated_at)
        timestamps['updated_at'] = local_updated_time.strftime('%Y-%m-%d %H:%M:%S')
    else:
        timestamps['updated_at'] = None

    return timestamps

def get_user(cart):
    """
    Helper function to retrieve user information.
    """
    user_info = cart.user
    if user_info:
        return {
            'id': user_info.id,
            'user_name': user_info.username,
        }
    return None

'''
def get_cart_response_data(cart, cart_items, user):
    """
    A helper function to format the cart response in the required structure.
    Optimized for performance.
    """
    # Prefetch related data to avoid repeated queries
    variants = Prefetch('variant', queryset=ProductVariants.objects.select_related(
        'product').prefetch_related('images').all())
    
    cart_items = cart_items.prefetch_related(variants)
    
    items_data = []
    for cart_item in cart_items:
        variant = cart_item.variant
        product = variant.product
        
        # Calculate item total in memory and avoid repeated function calls
        item_total = cart_item.calculate_price()

        items_data.append({
            "cart_item_id": cart_item.cart_item_id,
            'timestamps': get_timestamps(cart_item),
            "variant": {
                "variant_id": variant.pk,
                "variant_title": variant.variant_name,
                "variant_images": variant.images.first().image.url if variant.images.exists() else None,
                "item_price": cart_item.price,
                "product": {
                    "id": product.id,
                    "product_name": product.product_name,
                    "product_image": product.thumbnail.url if product.thumbnail else None
                }
            },
            "subtotal_amount": {
                "quantity": cart_item.quantity,
                "item_total": item_total,
            }
        })

    return {
        'cart_id': cart.cart_id,
        'timestamps': get_timestamps(cart),
        'user': get_user(cart),
        'cart_items': items_data
    }
------------------------------------------------------
def get_cart_response_data(cart, cart_items, user):
    """
    A helper function to format the cart response in the required structure.
    This is reused in both GET and POST responses.
    """
    items_data = []
    for cart_item in cart_items:
        items_data.append({
            "cart_item_id": cart_item.cart_item_id,
            'timestamps': get_timestamps(cart_item),
            "variant": {
                "variant_id": cart_item.variant.pk,
                "variant_title": cart_item.variant.variant_name,
                "thumbnail": cart_item.variant.images.first().image.url if cart_item.variant.images.exists() else None,
                "item_price": cart_item.price,
                "product": {
                    "id": cart_item.variant.product.id,
                    "product_name": cart_item.variant.product.product_name,
                    "product_image": cart_item.variant.product.thumbnail.url if cart_item.variant.product.thumbnail else None
                }
            },
            "subtotal_amount": {
                "quantity": cart_item.quantity,
                "item_total": cart_item.calculate_price(),
            }
        })

    return {
        'cart_id': cart.cart_id,
        'timestamps': get_timestamps(cart),
        'user': get_user(cart),
        'cart_items': items_data
    }
'''