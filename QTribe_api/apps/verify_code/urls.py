"""
验证码URL配置
"""

from django.urls import path
from verify_code.views import SendSmsCodeView, CheckSmsCodeView

urlpatterns = [
    path('send/', SendSmsCodeView.as_view(), name='send_sms'),
    path('check/', CheckSmsCodeView.as_view(), name='check_sms'),
]
