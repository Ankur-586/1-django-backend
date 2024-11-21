from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from django.db.models import Q

from .models import *
from .serializers import *

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(Q(is_active=True)).select_related('category', 'tax').prefetch_related('variants__images', 'tags')
    # queryset = Product.objects.filter(Q(is_active=True)).order_by('created_at')
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                data = self.get_paginated_response(serializer.data).data  # Use paginated response data
            else:
                serializer = self.get_serializer(queryset, many=True)
                data = serializer.data
            payload = {
                "status": status.HTTP_200_OK, 
                "message": 'All Products', 
                "data": data
            }
            return Response(payload ,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST, 
                "message": str(e), 
                "data": []
            }, status=status.HTTP_400_BAD_REQUEST)
    
