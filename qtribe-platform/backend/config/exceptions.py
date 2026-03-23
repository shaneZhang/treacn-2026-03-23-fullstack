from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        error_code = getattr(exc, 'default_code', 'error')
        error_detail = response.data

        if isinstance(error_detail, dict):
            message = error_detail.get('detail', str(error_detail))
        elif isinstance(error_detail, list):
            message = error_detail[0] if error_detail else 'Unknown error'
        else:
            message = str(error_detail)

        response.data = {
            'code': response.status_code,
            'message': message,
            'data': None,
            'error': {
                'code': error_code,
                'detail': error_detail
            }
        }
    else:
        response = Response(
            {
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Internal server error',
                'data': None,
                'error': {
                    'code': 'internal_error',
                    'detail': str(exc)
                }
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response


class BusinessException(Exception):
    def __init__(self, code=400, message='Business error', data=None):
        self.code = code
        self.message = message
        self.data = data
        super().__init__(self.message)
