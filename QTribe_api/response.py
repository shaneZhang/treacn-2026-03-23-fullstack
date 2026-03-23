"""
统一API响应格式
"""

from typing import Any, Optional
from rest_framework.response import Response
from rest_framework import status


class APIResponse(Response):
    def __init__(
        self,
        code: int = 200,
        message: str = 'success',
        data: Optional[Any] = None,
        success: bool = True,
        status_code: int = status.HTTP_200_OK,
        headers: Optional[dict] = None,
        **kwargs
    ):
        response_data = {
            'code': code,
            'message': message,
            'data': data,
            'success': success,
        }
        response_data.update(kwargs)
        
        super().__init__(
            data=response_data,
            status=status_code,
            headers=headers
        )
    
    @classmethod
    def success(cls, data: Any = None, message: str = '操作成功', **kwargs):
        return cls(
            code=200,
            message=message,
            data=data,
            success=True,
            **kwargs
        )
    
    @classmethod
    def error(cls, code: int = 400, message: str = '操作失败', data: Any = None, **kwargs):
        return cls(
            code=code,
            message=message,
            data=data,
            success=False,
            status_code=status.HTTP_400_BAD_REQUEST,
            **kwargs
        )
    
    @classmethod
    def created(cls, data: Any = None, message: str = '创建成功'):
        return cls(
            code=201,
            message=message,
            data=data,
            success=True,
            status_code=status.HTTP_201_CREATED
        )
    
    @classmethod
    def no_content(cls, message: str = '删除成功'):
        return cls(
            code=204,
            message=message,
            data=None,
            success=True,
            status_code=status.HTTP_204_NO_CONTENT
        )


class PaginatedResponse(Response):
    def __init__(
        self,
        items: list,
        total: int,
        page: int,
        page_size: int,
        message: str = 'success'
    ):
        total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0
        
        response_data = {
            'code': 200,
            'message': message,
            'success': True,
            'data': {
                'items': items,
                'pagination': {
                    'total': total,
                    'page': page,
                    'page_size': page_size,
                    'total_pages': total_pages,
                    'has_next': page < total_pages,
                    'has_previous': page > 1,
                }
            }
        }
        
        super().__init__(data=response_data)
