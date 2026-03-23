from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            'code': response.status_code,
            'message': response.data.get('detail', str(exc)),
            'data': {}
        }
    else:
        response = Response({
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'message': str(exc),
            'data': {}
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return response
