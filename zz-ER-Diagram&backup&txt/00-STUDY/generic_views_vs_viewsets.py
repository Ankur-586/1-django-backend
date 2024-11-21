'''
---------------
Generic Views:
---------------

Generic views are a set of pre-built views that DRF provides for common patterns in API development. 
They allow you to quickly create views for CRUD (Create, Read, Update, Delete) operations by specifying a few attributes and methods.

Common Generic Views:
--------------------
. ListAPIView: For listing multiple objects.
. CreateAPIView: For creating a new object.
. RetrieveAPIView: For retrieving a single object by its ID.
. UpdateAPIView: For updating an existing object.
. DestroyAPIView: For deleting an object.
. ListCreateAPIView: For listing objects and creating a new one.
. RetrieveUpdateAPIView: For retrieving and updating an object.
. RetrieveDestroyAPIView: For retrieving and deleting an object.
. RetrieveUpdateDestroyAPIView: For retrieving, updating, and deleting an object.

from rest_framework import generics
from .models import Category
from .serializers import CategorySerializer

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

When to Use:
-------------
. When you need to create views for standard CRUD operations without requiring complex logic.
. When you want to keep your code simple and adhere to common patterns.
. When you need fine-grained control over each specific action, such as customizing the behavior for listing or updating.
'''
# -------------------------------------- Generic Views vs Viewsets ---------------------------------------
'''
----------
Viewsets:
----------

Viewsets are a higher-level abstraction provided by DRF that combine multiple actions into a single class. 
They are typically used with routers to automatically generate the appropriate URLs and actions.

Common Viewsets:
---------------
. ModelViewSet: Provides default implementations for CRUD operations (list, create, retrieve, update, delete) on a model.
. ReadOnlyModelViewSet: Provides default implementations for read-only operations (list and retrieve) on a model.

from rest_framework import viewsets
from .models import Category
from .serializers import CategorySerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
With this CategoryViewSet, you get the following routes automatically:
. GET /categories/ (list)
. POST /categories/ (create)
. GET /categories/{id}/ (retrieve)
. PUT /categories/{id}/ (update)
. PATCH /categories/{id}/ (partial update)
. DELETE /categories/{id}/ (delete)

When to Use:
------------
. When you want to handle multiple actions (e.g., list, create, retrieve, update, delete) within a single class.
. When you prefer to use routers for automatically generating URL patterns, reducing boilerplate code.
. When you want to follow RESTful principles more closely with a single, unified class for a model.
'''
# -------------------------------------- Summary ---------------------------------------
'''
Generic Views:
--------------
. Provide individual views for different actions (e.g., list, create, retrieve).
. Offer more control over each action but require more boilerplate code.
. Suitable for simpler APIs or when you need to customize behavior for specific actions.

Viewsets:
----------
. Combine multiple actions into a single class.
. Work well with routers to automatically generate URLs.
. Suitable for more comprehensive APIs where you want to handle multiple actions in a unified manner.

Choosing Between Generic Views and Viewsets
--------------------------------------------
Use Generic Views: When you need to define actions separately, want more control over each action, 
or have specific customization needs for different endpoints.

Use Viewsets: When you prefer a more concise and unified way to handle multiple actions on a model, 
and you want to leverage DRF’s router system for automatic URL routing.
'''