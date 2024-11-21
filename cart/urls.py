from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartViewSet, CartItemPostSet, AssociateUserWithCart, CartItemUpdateSet

router = DefaultRouter()

# router.register(r'cart_items', CartItemViewSet)
router.register('post_cart', CartItemPostSet)
router.register('user_cart', AssociateUserWithCart, basename='carts') # pass cart id 
# router.register('cart_update/<uuid:cart_id>/', CartItemUpdateSet, basename='update-item-in-cart')

urlpatterns = [
    path('', include(router.urls)),
    path('cart/<str:cart_id>/', CartViewSet.as_view(), name='cart-detail'),
    path('user_cart/<str:cart_id>/', AssociateUserWithCart.as_view({'patch': 'update'}), name='associate-user-with-cart'),
    path('cart_update/<str:cart_id>/<int:variant_id>/', CartItemUpdateSet.as_view({'patch': 'partial_update'}), name='update-item-in-cart'),
]


