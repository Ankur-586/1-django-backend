from django.contrib import admin
from .models import *

@admin.register(UserProfile)
class user_profile(admin.ModelAdmin):
    list_display = ['user','profile_image','phone_number','created_at','updated_at']

@admin.register(User_Address)
class user_address(admin.ModelAdmin):
    list_display = ['user_profile', 'address_type', 'full_address']
    list_filter = ('country', 'state', 'address_type')
    search_fields = ('street_address', 'city', 'postal_code', 'user__user__username', 'user__user__email')



# from django.contrib.auth import get_user_model

# User = get_user_model()

# # Create a new user
# new_user = User.objects.create_user(email='test1@gmail.com', username='test1', password='intex123')