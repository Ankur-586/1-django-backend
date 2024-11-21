from user_auth.models import CustomUser, Role
from user_auth.serializers import UserSerializer
from .models import UserProfile, User_Address

from rest_framework import serializers

class UserAddressSerializers(serializers.ModelSerializer):
    class Meta:
        model = User_Address
        fields = ['full_address']

class UserProfileSerializers(serializers.ModelSerializer):
    user = UserSerializer()
    addresses = UserAddressSerializers(many=True, source='user_full_info')
    class Meta:
        model = UserProfile
        fields = ['user','profile_image','addresses']
