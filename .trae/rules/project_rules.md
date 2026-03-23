# QTribe 项目规则

## 项目概述
这是一个前后端分离的博客社交平台项目。

## 技术栈

### 后端 (QTribe_api)
- Django 4.2 + Django REST Framework
- JWT 认证 (djangorestframework-simplejwt)
- MySQL 数据库
- Redis 缓存

### 前端 (qtribe-web)
- React 18 + TypeScript (严格模式)
- Vite 构建工具
- Tailwind CSS
- React Query 数据请求
- Zustand 状态管理

## 开发命令

### 后端
```bash
cd QTribe_api
python manage.py runserver  # 启动开发服务器
python manage.py makemigrations  # 创建迁移
python manage.py migrate  # 执行迁移
python manage.py test  # 运行测试
```

### 前端
```bash
cd qtribe-web
npm run dev  # 启动开发服务器
npm run build  # 构建生产版本
npm run lint  # 代码检查
npm run typecheck  # TypeScript 类型检查
```

## 代码规范

### TypeScript
- 严格模式，禁止使用 any 类型
- 所有函数和变量必须有明确的类型定义
- 使用接口定义数据结构

### API 响应格式
```json
{
  "code": 200,
  "message": "success",
  "data": {},
  "success": true
}
```

### 分页格式
```json
{
  "items": [],
  "pagination": {
    "total": 100,
    "page": 1,
    "page_size": 10,
    "total_pages": 10,
    "has_next": true,
    "has_previous": false
  }
}
```

## 目录结构

```
QTribe_api/
├── apps/           # 应用模块
│   ├── user/       # 用户模块
│   ├── pieces_info/ # 内容模块
│   └── verify_code/ # 验证码模块
├── settings.py     # 配置文件
├── urls.py         # URL 路由
├── middleware.py   # 中间件
├── response.py     # 响应格式
├── exceptions.py   # 异常处理
└── error_codes.py  # 错误码定义

qtribe-web/
├── src/
│   ├── api/        # API 请求
│   ├── components/ # 组件
│   ├── lib/        # 工具库
│   ├── pages/      # 页面
│   ├── stores/     # 状态管理
│   └── types/      # TypeScript 类型
└── package.json
```
