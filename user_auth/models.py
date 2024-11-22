from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.db import models
from django.utils import timezone
from user_auth.manager import CustomUserManager
from core.utils import validate_no_special_chars

class Role(models.Model):
    name = models.CharField(max_length=15, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=13, unique=True, blank=True, null=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=50, blank=True, validators=[validate_no_special_chars])
    last_name = models.CharField(max_length=50, blank=True)
    last_login = models.DateTimeField(null=True, blank=True) 
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
# how do i customize my simple jwt token payload django rest framework response
# how do i customize my simple jwt token django rest framework response
# https://www.freecodecamp.org/news/how-to-use-jwt-and-django-rest-framework-to-get-tokens/

'''
{
    "status": "",
    "message": "",
    "data": []
}
{
        "count": 300,
        "next": "https://url:8000/?date=&lang=en&limit=5&offset=0&page=3&search=",
        "previous": "https://url:8000/?date=&lang=en&limit=5&offset=0&page=1&search=",
        "results": []
    }
'''