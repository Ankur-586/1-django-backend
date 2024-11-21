from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from core.utils import CustomValidation

def custom_exception_handler(exc, context):
    '''
    Custom Exception Handler: Catches exceptions raised within the defined routes. 
    In this case, when trying to access a product that doesn't exist, it triggers 
    an Http404 exception, which my handler captures.
    '''
    # Call DRF's default exception handler first
    response = exception_handler(exc, context)

    # Check for Http404 specifically
    if isinstance(exc, Http404):
        response_data = {
            'status': status.HTTP_404_NOT_FOUND,
            'message': 'The resource you are looking for was not found.',
            'data': []
        }
        return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    # Set default status code
    rep_status = status.HTTP_500_INTERNAL_SERVER_ERROR

    if response is not None:
        rep_status = response.status_code

        # Handle CustomValidation
        if isinstance(exc, CustomValidation):
            exc_list = str(exc).split("DETAIL: ")
            message = exc_list[-1] if exc_list else str(exc)
        else:
            # Handle other exceptions
            if isinstance(response.data, dict) and 'detail' in response.data:
                message = response.data['detail']
            else:
                message = 'An error occurred'
    else:
        # Handle cases where response is None
        message = "An unexpected error occurred"

    return Response({
        "status": rep_status,
        "message": message,
        "data": {}
    }, status=rep_status)

'''
if i do like http://127.0.0.1:8000/api/products/ds this, then i recieve the message from here 
BUT,
if i do like http://127.0.0.1:8000/api/product/ this, then i recieve message from utils custom_page_not_found_view
'''