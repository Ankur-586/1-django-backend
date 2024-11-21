# Not getting Used

from datetime import datetime
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import authentication, status
from rest_framework.exceptions import AuthenticationFailed, ParseError

from core.utils import CustomValidation

User = get_user_model()

class IsAuthenticated(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Extract the JWT from the Authorization header
        jwt_token = request.META.get('HTTP_AUTHORIZATION')
        if not jwt_token:
            raise CustomValidation("No token passed in request headers", 
                                   status_code=status.HTTP_401_UNAUTHORIZED)

        jwt_token = self.get_token_from_header(jwt_token)
        
        # Decode the JWT and verify its signature
        try:
            payload = self.decode_token(jwt_token)
        except AuthenticationFailed as e:
            raise e
        except ParseError as e:
            raise e

        # Get the user from the database
        user_identifier = payload.get('customer_id')  # Changed from 'user_id' to 'customer_id'
        if not user_identifier:
            raise AuthenticationFailed('User id not found in JWT')

        user = User.objects.filter(id=user_identifier).first()  # Query by user id
        if not user:
            raise AuthenticationFailed('User not found')
        return user, payload

    @staticmethod
    def get_token_from_header(header):
        # Extract the token from the header
        if header.startswith('Bearer '):
            return header[len('Bearer '):].strip()
        return header.strip()

    @staticmethod
    def decode_token(jwt_token):
        # Decode the JWT and verify its signature
        try:
            return jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            raise CustomValidation('Invalid signature', 
                                   status_code=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.ExpiredSignatureError:
            raise CustomValidation('Token has expired', 
                                   status_code=status.HTTP_401_UNAUTHORIZED)
        except jwt.DecodeError as e:
            raise CustomValidation(f'Error decoding token: {str(e)}', 
                                   status_code=status.HTTP_401_UNAUTHORIZED)

class JWTAuthentication(IsAuthenticated):
    def authenticate_header(self, request):
        return 'Bearer'

    @staticmethod
    def create_access_token(user):
        # Create the JWT payload
        payload = {
            'customer_id': user.id,
            'exp': int((datetime.now() + settings.JWT_CONF['ACCESS_TOKEN_LIFETIME']).timestamp()),
            'iat': datetime.now().timestamp(),
        }
        # Encode the JWT with your secret key
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

'''
views
from time import strftime
current_time = strftime("%H:%M:%S")

# class ObtainTokenView(views.APIView):
#     permission_classes = [permissions.AllowAny]
#     serializer_class = ObtainTokenSerializer

#     def post(self, request, *args, **kwargs):
#         try:
#             serializer = self.serializer_class(data=request.data)
            
#             # Validate serializer input
#             if not serializer.is_valid():
#                 return Response({
#                     "status_code": status.HTTP_400_BAD_REQUEST,
#                     "message": "Invalid input",
#                     "data": serializer.errors
#                 }, status=status.HTTP_400_BAD_REQUEST)

#             email_or_phone_number = serializer.validated_data.get('email')
#             password = serializer.validated_data.get('password')

#             # Look up user by email or phone number
#             user = User.objects.filter(email=email_or_phone_number).first()
#             if user is None:
#                 user = User.objects.filter(phone_number=email_or_phone_number).first()

#             # Check if user exists and password matches
#             if user is None:
#                 return Response({
#                     "status_code": status.HTTP_400_BAD_REQUEST,
#                     "message": "User not found",
#                     "data": []
#                 }, status=status.HTTP_400_BAD_REQUEST)
            
#             if not user.check_password(password):
#                 return Response({
#                     "status_code": status.HTTP_400_BAD_REQUEST,
#                     "message": "Invalid password",
#                     "data": []
#                 }, status=status.HTTP_400_BAD_REQUEST)

#             # Generate the JWT token
#             jwt_token = JWTAuthentication.create_access_token(user)

#             # Return success response with the token
#             return Response({
#                 "status_code": status.HTTP_201_CREATED,
#                 "message": "Access token created successfully",
#                 "access_token": jwt_token,
#                 "created_at": now().isoformat()
#             }, status=status.HTTP_201_CREATED)

#         except Exception as e:
#             # logger.error(f"Authentication error: {e}")
#             return Response({
#                 "status_code": status.HTTP_400_BAD_REQUEST,
#                 "message": "An error occurred",
#                 "data": []
#             }, status=status.HTTP_400_BAD_REQUEST)
'''
'''
def authenticate(self, request):
        # Extract and clean the JWT from the Authorization header
        jwt_token = request.META.get('HTTP_AUTHORIZATION')
        if jwt_token is None:
            return None
        
        jwt_token = JWTAuthentication.get_the_token_from_header(jwt_token)
        print('jwt_token',jwt_token)
        # Decode the JWT and verify its signature
        try:
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed('Invalid signature')
        except jwt.exceptions.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.DecodeError:
            raise ParseError('Error decoding token')

        # Get the user from the database
        email_or_phone_number = payload.get('user_identifier')
        if email_or_phone_number is None:
            raise AuthenticationFailed('User identifier not found in JWT')

        user = User.objects.filter(email=email_or_phone_number).first()
        if user is None:
            user = User.objects.filter(phone=email_or_phone_number).first()
        if user is None:
            raise AuthenticationFailed('User not found')

        return user, payload

    def authenticate_header(self, request):
        return 'Bearer'

    @classmethod
    def create_jwt(cls, user):
        # Create the JWT payload
        payload = {
            'customer_id': user.id,
            'exp': int((datetime.now() + settings.JWT_CONF['ACCESS_TOKEN_LIFETIME']).timestamp()),
            'iat': datetime.now().timestamp(),
            # 'email': user.email,
            # 'phone_number': user.phone_number,
        }
        # Encode the JWT with your secret key
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    @classmethod
    def get_the_token_from_header(cls, token):
        return token.replace('Bearer', '').strip()
'''