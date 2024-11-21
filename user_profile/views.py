from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import UserProfile
from .serializers import UserProfileSerializers, UserAddressSerializers

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all().order_by('created_at')
    serializer_class = UserProfileSerializers 
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # If the user is an admin, return all user profiles
        print(self.request.user)
        if self.request.user.is_staff:
            return UserProfile.objects.all()
        # Otherwise, return only the authenticated user's profile
        return UserProfile.objects.filter(user=self.request.user)
    
'''
if self.request.user.is_staff:
    print(True)
else:
    print(False)
'''