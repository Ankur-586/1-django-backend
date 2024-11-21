from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

from . import views

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
# router.register(r'products')

urlpatterns = [
    path('', include(router.urls)),
    # path('test', views.test, name='test'),
]
