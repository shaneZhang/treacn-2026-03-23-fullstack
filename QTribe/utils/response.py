from rest_framework.response import Response
from rest_framework import status

class APIResponse(Response):
    def __init__(self, data=None, code=status.HTTP_200_OK, message='success', **kwargs):
        response_data = {
            'code': code,
            'message': message,
            'data': data if data is not None else {}
        }
        super().__init__(response_data, **kwargs)

class SuccessResponse(APIResponse):
    def __init__(self, data=None, message='success', **kwargs):
        super().__init__(data=data, code=status.HTTP_200_OK, message=message, **kwargs)

class CreatedResponse(APIResponse):
    def __init__(self, data=None, message='created successfully', **kwargs):
        super().__init__(data=data, code=status.HTTP_201_CREATED, message=message, **kwargs)

class BadRequestResponse(APIResponse):
    def __init__(self, message='bad request', **kwargs):
        super().__init__(code=status.HTTP_400_BAD_REQUEST, message=message, **kwargs)

class UnauthorizedResponse(APIResponse):
    def __init__(self, message='unauthorized', **kwargs):
        super().__init__(code=status.HTTP_401_UNAUTHORIZED, message=message, **kwargs)

class ForbiddenResponse(APIResponse):
    def __init__(self, message='forbidden', **kwargs):
        super().__init__(code=status.HTTP_403_FORBIDDEN, message=message, **kwargs)

class NotFoundResponse(APIResponse):
    def __init__(self, message='not found', **kwargs):
        super().__init__(code=status.HTTP_404_NOT_FOUND, message=message, **kwargs)

class ServerErrorResponse(APIResponse):
    def __init__(self, message='server error', **kwargs):
        super().__init__(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=message, **kwargs)
