"""
错误码定义
"""

from enum import Enum


class ErrorCode(Enum):
    SUCCESS = (200, '操作成功')
    CREATED = (201, '创建成功')
    NO_CONTENT = (204, '删除成功')
    
    BAD_REQUEST = (400, '请求参数错误')
    UNAUTHORIZED = (401, '未授权访问')
    FORBIDDEN = (403, '权限不足')
    NOT_FOUND = (404, '资源不存在')
    METHOD_NOT_ALLOWED = (405, '请求方法不允许')
    CONFLICT = (409, '资源冲突')
    TOO_MANY_REQUESTS = (429, '请求过于频繁')
    
    INTERNAL_ERROR = (500, '服务器内部错误')
    SERVICE_UNAVAILABLE = (503, '服务暂不可用')
    
    VALIDATION_ERROR = (4001, '数据验证失败')
    AUTHENTICATION_FAILED = (4002, '认证失败')
    PERMISSION_DENIED = (4003, '权限不足')
    RESOURCE_NOT_FOUND = (4004, '资源不存在')
    RATE_LIMIT_EXCEEDED = (4005, '请求频率超限')
    
    USER_NOT_FOUND = (5001, '用户不存在')
    USER_ALREADY_EXISTS = (5002, '用户已存在')
    USERNAME_EXISTS = (5003, '用户名已存在')
    PHONE_EXISTS = (5004, '手机号已注册')
    EMAIL_EXISTS = (5005, '邮箱已注册')
    PASSWORD_ERROR = (5006, '密码错误')
    PASSWORD_NOT_MATCH = (5007, '两次密码不一致')
    
    ARTICLE_NOT_FOUND = (5101, '文章不存在')
    VIDEO_NOT_FOUND = (5102, '视频不存在')
    COMMENT_NOT_FOUND = (5103, '评论不存在')
    LIFE_NOT_FOUND = (5104, '生活分享不存在')
    
    SMS_SEND_FAILED = (5201, '短信发送失败')
    SMS_CODE_EXPIRED = (5202, '验证码已过期')
    SMS_CODE_ERROR = (5203, '验证码错误')
    
    FILE_UPLOAD_FAILED = (5301, '文件上传失败')
    FILE_TYPE_ERROR = (5302, '文件类型不支持')
    FILE_SIZE_ERROR = (5303, '文件大小超出限制')
    
    ALREADY_STARRED = (5401, '已经点赞过了')
    ALREADY_COLLECTED = (5402, '已经收藏过了')
    ALREADY_FOLLOWED = (5403, '已经关注过了')
    ALREADY_FRIEND = (5404, '已经是好友了')
    
    NOT_STARRED = (5411, '尚未点赞')
    NOT_COLLECTED = (5412, '尚未收藏')
    NOT_FOLLOWED = (5413, '尚未关注')
    NOT_FRIEND = (5414, '还不是好友')
    
    @classmethod
    def get_message(cls, code: int) -> str:
        for error in cls:
            if error.value[0] == code:
                return error.value[1]
        return '未知错误'
