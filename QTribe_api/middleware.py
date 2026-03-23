"""
安全中间件
"""

import time
import redis
import bleach
from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class XSSProtectionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method in ['POST', 'PUT', 'PATCH']:
            if hasattr(request, 'data') and isinstance(request.data, dict):
                self._sanitize_data(request.data)
    
    def _sanitize_data(self, data):
        allowed_tags = []
        allowed_attributes = {}
        
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = bleach.clean(
                    value,
                    tags=allowed_tags,
                    attributes=allowed_attributes,
                    strip=True
                )
            elif isinstance(value, dict):
                self._sanitize_data(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        self._sanitize_data(item)


class RateLimitMiddleware(MiddlewareMixin):
    redis_client = None
    
    def __init__(self, get_response=None):
        self.get_response = get_response
        try:
            self.redis_client = redis.Redis(
                host=getattr(settings, 'REDIS_HOST', 'localhost'),
                port=getattr(settings, 'REDIS_PORT', 6379),
                db=getattr(settings, 'REDIS_RATE_LIMIT_DB', 3),
                decode_responses=True
            )
        except Exception:
            pass
    
    def process_request(self, request):
        if not self.redis_client:
            return None
        
        if request.path.startswith('/admin/') or request.path.startswith('/api/v1/auth/'):
            return None
        
        ip = self._get_client_ip(request)
        user_id = request.user.id if hasattr(request, 'user') and request.user.is_authenticated else None
        
        key = f'rate:{ip}'
        if user_id:
            key = f'rate:user:{user_id}'
        
        limit = getattr(settings, 'RATE_LIMIT_PER_MINUTE', 60)
        window = 60
        
        current = self.redis_client.get(key)
        
        if current and int(current) >= limit:
            return JsonResponse({
                'code': 429,
                'message': '请求过于频繁，请稍后再试',
                'success': False
            }, status=429)
        
        pipe = self.redis_client.pipeline()
        pipe.incr(key)
        pipe.expire(key, window)
        pipe.execute()
        
        return None
    
    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '0.0.0.0')


class RateLimiter:
    redis_client = None
    
    @classmethod
    def _get_redis(cls):
        if cls.redis_client is None:
            try:
                cls.redis_client = redis.Redis(
                    host=getattr(settings, 'REDIS_HOST', 'localhost'),
                    port=getattr(settings, 'REDIS_PORT', 6379),
                    db=getattr(settings, 'REDIS_RATE_LIMIT_DB', 3),
                    decode_responses=True
                )
            except Exception:
                pass
        return cls.redis_client
    
    @classmethod
    def check_rate_limit(cls, key: str, limit: int = 5, window: int = 60) -> bool:
        redis_client = cls._get_redis()
        if not redis_client:
            return True
        
        current = redis_client.get(key)
        if current and int(current) >= limit:
            return False
        
        pipe = redis_client.pipeline()
        pipe.incr(key)
        pipe.expire(key, window)
        pipe.execute()
        
        return True
    
    @classmethod
    def reset_rate_limit(cls, key: str):
        redis_client = cls._get_redis()
        if redis_client:
            redis_client.delete(key)
