from django.urls import path
from .views import CategoryListView, SubcategoryListView, CategoryDetailView
from . import views

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('subcategories/', SubcategoryListView.as_view(), name='subcategory-list'),
    path('categories/<int:pk>/subcategories/', CategoryDetailView.as_view(), name='category-detail'),
]

# when i am hitting right url and if there is some error in the code then it is working but when  i change the url to something then it is not woreking