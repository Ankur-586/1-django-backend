from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator

from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
import logging

from user_auth.models import CustomUser, Role
from core.utils import CustomValidation

# logger = logging.getLogger('user_auth')

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description']

class UserSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(
    #     required=True,
    #     validators=[UniqueValidator(queryset=CustomUser.objects.all(),
    #                 message='User with Email Already Exists!!')]
    # )
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        '''
        All the below fields are shown as a response 
        in a results list which contain dicts
        '''
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'password2', 
                  'user_role', 'last_login']
    
    def get_last_login(self, obj):
        '''
        This function converts timestamp in ISO 8601 format
        to a proper datetime formatted string
        '''
        if obj.last_login:
            local_time = timezone.localtime(obj.last_login)
            return local_time.strftime('%Y-%m-%d %H:%M:%S')
        return 'None'
    
    def validate(self, attrs):
        
        errors = {}
        # Check if passwords match
        if attrs['password'] != attrs['password2']:
            errors['password'] = "Password fields didn't match."
        
        # Check for unique email and username
        existing_users = CustomUser.objects.filter(email=attrs['email']) | CustomUser.objects.filter(username=attrs['username'])
        for user in existing_users:
            if user.email == attrs['email']:
                errors['email'] = "User with this email already exists!"
            if user.username == attrs['username']:
                errors['username'] = "Username already exists!"
        first_name = attrs['first_name']
        last_name = attrs['last_name']
        
        if not (first_name.isalnum() and last_name.isalnum()):  
            raise serializers.ValidationError('Only alphanumeric characters are allowed.')
        
        if errors:
            raise serializers.ValidationError(errors)
            # raise CustomValidation(errors, status_code=status.HTTP_400_BAD_REQUEST)

        return attrs
        
    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            # user_role=role,
            is_active=True
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class ObtainTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
    
# my serializer class UserSerializer(serializers.ModelSerializer): 
#     # email = serializers.EmailField(
#     #     required=True,
#     #     validators=[UniqueValidator(queryset=CustomUser.objects.all(),
#     #                 message='User with Email Already Exists!!')]
#     # )
#     email = serializers.EmailField(required=True)
#     username = serializers.CharField(required=True)
#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, required=True)
#     first_name = serializers.CharField()
#     last_name = serializers.CharField()

#     class Meta:
#         '''
#         All the below fields are shown as a response 
#         in a results list which contain dicts
#         '''
#         model = CustomUser
#         fields = ['email', 'username', 'first_name', 'last_name', 'password', 'password2', 
#                   'user_role', 'last_login']
    
#     def get_last_login(self, obj):
#         '''
#         This function converts timestamp in ISO 8601 format
#         to a proper datetime formatted string
#         '''
#         if obj.last_login:
#             local_time = timezone.localtime(obj.last_login)
#             return local_time.strftime('%Y-%m-%d %H:%M:%S')
#         return 'None'
    
#     def validate(self, attrs):
        
#         errors = {}
#         # Check if passwords match
#         if attrs['password'] != attrs['password2']:
#             errors['password'] = "Password fields didn't match."
        
#         # Check for unique email
#         if CustomUser.objects.filter(email=attrs['email']).exists():
#             errors['email'] = "User with this email already exists!"

#         # Check for unique username
#         if CustomUser.objects.filter(username=attrs['username']).exists():
#             errors['username'] = "Username already exists!"

#         if errors:
#             raise serializers.ValidationError(errors)
#             # raise CustomValidation(errors, status_code=status.HTTP_400_BAD_REQUEST)

#         return attrs
        
#     def create(self, validated_data):
#         validated_data.pop('password2')
#         user = CustomUser.objects.create(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name'],
#             # user_role=role,
#             is_active=True
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user and my view create method, now user creation is taking 3 seconds