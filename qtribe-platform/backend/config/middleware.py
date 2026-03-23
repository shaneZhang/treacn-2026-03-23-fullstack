import re
import time
from typing import Optional

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from django.conf import settings


class SecurityHeadersMiddleware(MiddlewareMixin):
    """添加安全相关的HTTP头"""

    def process_response(self, request, response):
        # XSS Protection
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'

        # Content Security Policy
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'",
            "style-src 'self' 'unsafe-inline'",
            "img-src 'self' data: https:",
            "font-src 'self'",
            "connect-src 'self'",
            "media-src 'self'",
            "object-src 'none'",
            "frame-ancestors 'none'",
            "base-uri 'self'",
            "form-action 'self'",
        ]
        response['Content-Security-Policy'] = '; '.join(csp_directives)

        return response


class RateLimitMiddleware(MiddlewareMixin):
    """API限流中间件"""

    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.rate_limit = getattr(settings, 'RATE_LIMIT', 100)
        self.rate_limit_window = getattr(settings, 'RATE_LIMIT_WINDOW', 60)

    def get_client_ip(self, request):
        """获取客户端IP地址"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_rate_limit_key(self, request):
        """生成限流的缓存键"""
        ip = self.get_client_ip(request)
        user_id = request.user.id if request.user.is_authenticated else 'anonymous'
        return f'rate_limit:{ip}:{user_id}:{request.path}'

    def process_request(self, request):
        """处理请求，检查是否超过限流"""
        # 跳过静态文件和管理后台
        if request.path.startswith('/static/') or request.path.startswith('/admin/'):
            return None

        # 跳过健康检查端点
        if request.path == '/health/':
            return None

        key = self.get_rate_limit_key(request)
        now = time.time()

        # 获取当前窗口的请求记录
        requests_data = cache.get(key, [])

        # 清理过期的请求记录
        requests_data = [req_time for req_time in requests_data
                        if now - req_time < self.rate_limit_window]

        # 检查是否超过限流
        if len(requests_data) >= self.rate_limit:
            return JsonResponse({
                'code': 429,
                'message': '请求过于频繁，请稍后再试',
                'data': None
            }, status=429)

        # 记录当前请求
        requests_data.append(now)
        cache.set(key, requests_data, self.rate_limit_window)

        return None


class CSRFProtectionMiddleware(MiddlewareMixin):
    """CSRF保护中间件"""

    def process_request(self, request):
        """验证CSRF Token"""
        # 跳过GET、HEAD、OPTIONS请求
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return None

        # 跳过登录和注册端点
        if request.path in ['/api/users/auth/login/', '/api/users/auth/register/']:
            return None

        # 检查CSRF Token
        csrf_token = request.headers.get('X-CSRF-Token')
        if not csrf_token:
            # 对于API请求，如果使用了JWT认证，可以放宽CSRF检查
            auth_header = request.headers.get('Authorization', '')
            if auth_header.startswith('Bearer '):
                return None

            return JsonResponse({
                'code': 403,
                'message': 'CSRF验证失败',
                'data': None
            }, status=403)

        return None


class XSSProtectionMiddleware(MiddlewareMixin):
    """XSS防护中间件"""

    # 危险字符和模式
    DANGEROUS_PATTERNS = [
        r'<script[^>]*>.*?</script>',
        r'javascript:',
        r'on\w+\s*=',
        r'<iframe[^>]*>',
        r'<object[^>]*>',
        r'<embed[^>]*>',
    ]

    def sanitize_string(self, value: str) -> str:
        """清理字符串中的危险内容"""
        if not isinstance(value, str):
            return value

        for pattern in self.DANGEROUS_PATTERNS:
            value = re.sub(pattern, '', value, flags=re.IGNORECASE | re.DOTALL)

        return value

    def sanitize_data(self, data):
        """递归清理数据"""
        if isinstance(data, dict):
            return {key: self.sanitize_data(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.sanitize_data(item) for item in data]
        elif isinstance(data, str):
            return self.sanitize_string(data)
        return data

    def process_request(self, request):
        """处理请求数据"""
        if request.content_type == 'application/json':
            try:
                import json
                body = request.body.decode('utf-8')
                if body:
                    data = json.loads(body)
                    sanitized_data = self.sanitize_data(data)
                    request._body = json.dumps(sanitized_data).encode('utf-8')
            except Exception:
                pass

        return None


class SQLInjectionProtectionMiddleware(MiddlewareMixin):
    """SQL注入防护中间件"""

    # SQL注入危险模式
    SQL_PATTERNS = [
        r'(\%27)|(\')|(\-\-)|(\%23)|(#)',
        r'((\%3D)|(=))[^\n]*((\%27)|(\')|(\-\-)|(\%3B)|(;))',
        r'\w*((\%27)|(\'))((\%6F)|o|(\%4F))((\%72)|r|(\%52))',
        r'((\%27)|(\'))union',
        r'exec(\s|\+)+(s|x)p\w+',
        r'UNION\s+SELECT',
        r'INSERT\s+INTO',
        r'DELETE\s+FROM',
        r'DROP\s+TABLE',
    ]

    def process_request(self, request):
        """检查请求参数是否包含SQL注入"""
        # 检查查询参数
        for key, values in request.GET.lists():
            for value in values:
                if self.contains_sql_injection(value):
                    return JsonResponse({
                        'code': 400,
                        'message': '请求参数包含非法字符',
                        'data': None
                    }, status=400)

        # 检查POST数据
        if request.method == 'POST':
            for key, values in request.POST.lists():
                for value in values:
                    if self.contains_sql_injection(value):
                        return JsonResponse({
                            'code': 400,
                            'message': '请求参数包含非法字符',
                            'data': None
                        }, status=400)

        return None

    def contains_sql_injection(self, value: str) -> bool:
        """检查字符串是否包含SQL注入"""
        if not isinstance(value, str):
            return False

        value = value.upper()
        for pattern in self.SQL_PATTERNS:
            if re.search(pattern, value, re.IGNORECASE):
                return True

        return False


class LoggingMiddleware(MiddlewareMixin):
    """请求日志中间件"""

    def process_request(self, request):
        """记录请求信息"""
        request.start_time = time.time()
        return None

    def process_response(self, request, response):
        """记录响应信息"""
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time

            # 记录慢请求
            if duration > 1.0:
                import logging
                logger = logging.getLogger('django.security.SlowRequest')
                logger.warning(
                    f'Slow request: {request.method} {request.path} - {duration:.2f}s'
                )

        return response
