from django.contrib.auth import get_user_model
from django.utils.timezone import now

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from .models import CustomUser
from .serializers import UserSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('-id')
    serializer_class = UserSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data # pagination data
        else:
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
        payload = {
            "status": status.HTTP_200_OK, 
            "message": 'All User Details', 
            "data": data
        }
        return Response(payload ,status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                "status": status.HTTP_201_CREATED,
                "message": 'User Created', 
                "data": serializer.data
                }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': serializer.errors,
                'data': []
            }, status=status.HTTP_400_BAD_REQUEST)

'''
def create(self, request, *args, **kwargs):
        errors = []
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                "status": status.HTTP_201_CREATED,
                "message": 'User Created', 
                "data": serializer.data
                }, status=status.HTTP_201_CREATED)
        else:
            errors.extend([
                    f"{field}: {message}"
                    for field, messages in serializer.errors.items()
                    for message in messages
                ])
        if errors:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': errors,
                'data': []
            }, status=status.HTTP_400_BAD_REQUEST)
'''