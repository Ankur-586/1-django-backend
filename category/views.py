from rest_framework import viewsets, generics, status
from rest_framework.response import Response

from django.db.models import Q

from .models import Category
from .serializers import CategorySerializer

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.filter(Q(parent_category__isnull=True) & Q(is_active=True))
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
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
                "message": 'All Categories', 
                "data": data
            }
            return Response(payload ,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": str(e),
                "data": []
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # Validate the data
        if serializer.is_valid():
            # If the data is valid, save the new category and return success response
            serializer.save()
            return Response({
                "status": status.HTTP_201_CREATED,
                "message": "Category created successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            # If validation fails, return the errors with a 400 Bad Request status
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Validation failed.",
                "data": serializer.errors  # Returning validation errors here
            }, status=status.HTTP_400_BAD_REQUEST)
    
# View to get all subcategories
class SubcategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(parent_category__isnull=True)
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
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
                "message": 'All Categories', 
                "data": data
            }
            return Response(payload ,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": str(e),
                "data": []
            }, status=status.HTTP_400_BAD_REQUEST)
    
# View to get a specific category and its subcategories by ID
class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    # def retrieve(self, request, *args, **kwargs):
    #     try:
    #         queryset = self.filter_queryset(self.get_queryset())
    #         page = self.paginate_queryset(queryset)
    #         if page is not None:
    #             serializer = self.get_serializer(page, many=True)
    #             result = self.get_paginated_response(serializer.data)
    #             data = result.data # pagination data
    #         else:
    #             serializer = self.get_serializer(queryset, many=True)
    #             data = serializer.data
    #         payload = {
    #             "status": status.HTTP_200_OK, 
    #             "message": 'Specific Category and its Subcategories by ID', 
    #             "data": data
    #         }
    #         return Response(payload ,status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({
    #             "status": status.HTTP_400_BAD_REQUEST,
    #             "message": str(e),
    #             "data": []
    #         }, status=status.HTTP_400_BAD_REQUEST)

'''
Do Not Delete.
https://zoejoyuliao.medium.com/django-rest-framework-add-custom-pagination-c758a4f127fa

Why Both Are Used:

payload Dictionary:
The payload dictionary contains a custom status_code field which is included in the response body. 
This is useful for providing additional context or information about the success or failure of the 
request within the body of the response.

status Parameter in Response:
The status parameter in the Response constructor sets the HTTP status code for the response. 
This is the code that will be sent as part of the HTTP response headers and is used to indicate 
the overall result of the HTTP request (e.g., 200 OK, 400 Bad Request, etc.).
'''