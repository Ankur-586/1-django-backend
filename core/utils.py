from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.response import Response

from django.utils.encoding import force_str
from django.conf import settings
from django.http import JsonResponse
from django.core.exceptions import ValidationError

''' ------------------------------------------------------------------ '''
class CustomValidation(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail, status_code):
        if status_code is not None:self.status_code = status_code
        if detail is not None:
            self.detail = force_str(detail)
        else: 
            self.detail = {'detail': force_str(self.default_detail)}
''' ------------------------------------------------------------------ '''
def error_response(message, status_code):
        """
        Helper method to return a standard error response.
        """
        return Response({
            'status': status_code,
            'message': message,
            'data': []
        }, status=status_code)
'''--------------------------------------------------------------------'''
def validate_no_special_chars(value):
        if not value.isalnum():  
            raise ValidationError('Only alphanumeric characters are allowed.')
'''---------------------------------------------------------------------'''

def construct_full_url(relative_url):
    """
    Constructs a full URL given a relative URL.
    
    :param relative_url: The relative URL of the media file.
    :return: The full URL or None if the relative_url is empty.
    """
    if relative_url:
        return f"{settings.BASE_URL}{relative_url}"
    return None
''' ------------------------------------------------------------------ '''
def custom_page_not_found_view(request, exception=None):
    '''
    Custom 404 Handler: Catches all requests that do not match any defined URL patterns.
    '''
    response_data = {
        'status': status.HTTP_404_NOT_FOUND,
        'message': f'Coming From Utils.py: The resource you are looking for was not found.',
        'data': []
    }
    return JsonResponse(response_data, status=status.HTTP_404_NOT_FOUND)
'''-----------------------------------------------------------------------'''

