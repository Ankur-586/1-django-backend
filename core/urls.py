"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from .utils import custom_page_not_found_view

'''
The below handler is only working when debug is set to FALSE.
But, there is a catch. Look inside custome handler
'''
handler404 = custom_page_not_found_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('user_auth.urls')),
    path('api/',include('user_profile.urls')),
    path('api/',include('category.urls')),
    path('api/',include('product.urls')),
    path('api/',include('order.urls')),
    path('api/',include('cart.urls')),
    # path('api-auth/', include('rest_framework.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
