"""
验证码视图
"""

import random
import string
import redis
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.conf import settings

from QTribe_api.response import APIResponse
from QTribe_api.exceptions import ValidationError, RateLimitError
from QTribe_api.middleware.rate_limit import RateLimiter


class SendSmsCodeView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        phone = request.data.get('phone')
        
        if not phone:
            raise ValidationError('手机号不能为空')
        
        if not phone.startswith('1') or len(phone) != 11:
            raise ValidationError('手机号格式不正确')
        
        rate_key = f'rate:sms:{phone}'
        if not RateLimiter.check_rate_limit(rate_key, limit=5, window=60):
            raise RateLimitError('发送过于频繁，请稍后再试')
        
        code = ''.join(random.choices(string.digits, k=6))
        
        try:
            redis_conn = redis.Redis(
                host=settings.REDIS_VERIFY_CODE['host'],
                port=settings.REDIS_VERIFY_CODE['port'],
                db=settings.REDIS_VERIFY_CODE['db'],
                decode_responses=True
            )
            redis_conn.setex(f'sms:{phone}', 300, code)
        except Exception:
            pass
        
        return APIResponse.success(
            data={'code': code},
            message='验证码发送成功'
        )


class CheckSmsCodeView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        phone = request.data.get('phone')
        code = request.data.get('code')
        
        if not phone or not code:
            raise ValidationError('手机号和验证码不能为空')
        
        try:
            redis_conn = redis.Redis(
                host=settings.REDIS_VERIFY_CODE['host'],
                port=settings.REDIS_VERIFY_CODE['port'],
                db=settings.REDIS_VERIFY_CODE['db'],
                decode_responses=True
            )
            stored_code = redis_conn.get(f'sms:{phone}')
        except Exception:
            stored_code = None
        
        if not stored_code:
            raise ValidationError('验证码已过期')
        
        if stored_code != code:
            raise ValidationError('验证码错误')
        
        redis_conn.delete(f'sms:{phone}')
        
        return APIResponse.success(message='验证成功')
