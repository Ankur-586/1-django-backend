from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_info")
    profile_image = models.ImageField(upload_to="user_profile")
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'

ADDRESS_TYPES = (
        ('home', _('Home')),
        ('work', _('Work')),
        ('other', _('Other')),
    )

class User_Address(models.Model):
    user_profile = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="user_full_info")
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPES)
    house_number = models.CharField(max_length=10)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=6)
    country = models.CharField(default='India',max_length=5)

    def clean(self):
        self.pin_code_validate()

    def pin_code_validate(self):
        if not self.postal_code.isdigit() or len(self.postal_code) != 6:
            raise ValidationError('Postal code must be a 6-digit number.')
    
    @property
    def full_address(self):
        return f'''{self.house_number}, {self.address_line_1}, {self.address_line_2}, {self.city}, {self.state}, {self.postal_code}, {self.country}'''.strip()
                    
    def __str__(self):
        return f'{self.user_profile} Address'
    