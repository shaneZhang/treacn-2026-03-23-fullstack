"""
自定义异常处理
"""

from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework import status
from response import APIResponse


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        error_code = response.status_code
        error_msg = ''
        
        if isinstance(response.data, dict):
            if 'detail' in response.data:
                error_msg = response.data['detail']
            elif 'message' in response.data:
                error_msg = response.data['message']
            else:
                error_msg = str(response.data)
        elif isinstance(response.data, list):
            error_msg = '; '.join([str(item) for item in response.data])
        else:
            error_msg = str(response.data)
        
        return APIResponse(
            code=error_code,
            message=error_msg,
            data=None,
            success=False
        )
    
    return APIResponse(
        code=500,
        message='服务器内部错误',
        data=None,
        success=False
    )


class BusinessException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '业务异常'
    default_code = 'business_error'
    
    def __init__(self, code: int = 400, message: str = '业务异常', data=None):
        self.code = code
        self.message = message
        self.data = data
        super().__init__(detail=message, code=code)


class ValidationError(BusinessException):
    def __init__(self, message: str = '数据验证失败', data=None):
        super().__init__(code=4001, message=message, data=data)


class AuthenticationError(BusinessException):
    def __init__(self, message: str = '认证失败', data=None):
        super().__init__(code=4002, message=message, data=data)


class PermissionError(BusinessException):
    def __init__(self, message: str = '权限不足', data=None):
        super().__init__(code=4003, message=message, data=data)


class NotFoundError(BusinessException):
    def __init__(self, message: str = '资源不存在', data=None):
        super().__init__(code=4004, message=message, data=data)


class RateLimitError(BusinessException):
    def __init__(self, message: str = '请求过于频繁，请稍后再试', data=None):
        super().__init__(code=4005, message=message, data=data)
