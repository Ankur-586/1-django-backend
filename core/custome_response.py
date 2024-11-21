from rest_framework.response import Response

class CustomResponse(Response):
    """
    A custom response class for Django REST Framework that adds a `status_code`
    attribute to the response data.
    """
    def __init__(self, data=None, status_code=None, message=None, **kwargs):
        # Ensure data is a dictionary and contains the necessary fields
        response_data = {
            'status_code': status_code if status_code is not None else 200,
            'message': message if message is not None else "",
            'data': data if data is not None else []
        }
        # Initialize the parent Response class
        super().__init__(data=response_data, **kwargs)

