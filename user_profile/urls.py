from django.urls import path,include

from rest_framework import routers

from .views import UserProfileViewSet


router = routers.DefaultRouter()
router.register('user_profile', UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
