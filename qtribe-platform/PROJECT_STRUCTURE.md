# QTribe 项目结构

## 项目概述
QTribe 是一个前后端分离的博客社交平台，采用 Django REST Framework + React + TypeScript 技术栈。

## 目录结构

```
qtribe-platform/
├── backend/                    # Django 后端
│   ├── apps/                  # 应用模块
│   │   ├── users/            # 用户模块
│   │   │   ├── models.py     # 用户模型
│   │   │   ├── serializers.py # 序列化器
│   │   │   ├── views.py      # 视图
│   │   │   └── urls.py       # 路由
│   │   ├── articles/         # 文章模块
│   │   │   ├── models.py     # 文章模型
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   └── urls.py
│   │   └── interactions/     # 互动模块（点赞、收藏、通知）
│   │       ├── models.py
│   │       ├── serializers.py
│   │       ├── views.py
│   │       └── urls.py
│   ├── config/               # 项目配置
│   │   ├── settings/         # 配置文件
│   │   │   ├── base.py      # 基础配置
│   │   │   ├── local.py     # 本地开发配置
│   │   │   └── production.py # 生产环境配置
│   │   ├── middleware.py     # 自定义中间件
│   │   ├── pagination.py     # 分页配置
│   │   ├── exceptions.py     # 异常处理
│   │   ├── urls.py           # 主路由
│   │   └── wsgi.py
│   ├── manage.py
│   ├── requirements.txt      # Python 依赖
│   └── .env.example          # 环境变量示例
│
├── frontend/                  # React 前端
│   ├── src/
│   │   ├── components/       # 公共组件
│   │   │   ├── Layout.tsx    # 布局组件
│   │   │   └── ProtectedRoute.tsx # 路由保护
│   │   ├── pages/            # 页面组件
│   │   │   ├── HomePage.tsx
│   │   │   ├── LoginPage.tsx
│   │   │   ├── RegisterPage.tsx
│   │   │   ├── ArticleListPage.tsx
│   │   │   ├── ArticleDetailPage.tsx
│   │   │   ├── ArticleCreatePage.tsx
│   │   │   └── ProfilePage.tsx
│   │   ├── services/         # API 服务
│   │   │   ├── api.ts        # 基础 API 配置
│   │   │   ├── auth.service.ts
│   │   │   ├── article.service.ts
│   │   │   └── interaction.service.ts
│   │   ├── stores/           # 状态管理
│   │   │   └── auth.store.ts # 认证状态
│   │   ├── types/            # TypeScript 类型
│   │   │   └── index.ts
│   │   ├── utils/            # 工具函数
│   │   │   └── security.ts   # 安全相关
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── public/
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── .env.example
│
├── start.sh                   # 启动脚本
└── PROJECT_STRUCTURE.md       # 本文件
```

## 技术栈

### 后端
- **框架**: Django 4.2 + Django REST Framework
- **认证**: JWT (django-rest-framework-simplejwt)
- **数据库**: MySQL
- **缓存**: Redis (django-redis)
- **文档**: drf-spectacular (OpenAPI/Swagger)
- **其他**: django-cors-headers, django-filter

### 前端
- **框架**: React 18 + TypeScript (严格模式)
- **构建工具**: Vite
- **状态管理**: Zustand
- **数据获取**: TanStack Query (React Query)
- **路由**: React Router
- **样式**: Tailwind CSS
- **图标**: Lucide React

## 核心功能

### P0 功能（已完成）
1. **用户认证**
   - 注册/登录/登出
   - JWT Token 认证
   - 个人资料管理

2. **文章管理**
   - 文章 CRUD
   - 文章列表/详情
   - 标签管理
   - 评论系统

3. **互动功能**
   - 点赞/取消点赞
   - 收藏/取消收藏
   - 通知系统

4. **个人中心**
   - 我的文章
   - 我的收藏
   - 我的点赞
   - 个人设置

## 安全特性

### 后端安全
- XSS 防护中间件
- SQL 注入防护
- CSRF 保护
- 请求限流 (Rate Limiting)
- 安全 HTTP 头
- Content Security Policy

### 前端安全
- 输入消毒
- XSS 过滤
- 文件类型验证
- 文件大小限制
- CSRF Token 管理
- 请求限流

## API 设计

### 认证相关
- `POST /api/users/auth/login/` - 登录
- `POST /api/users/auth/register/` - 注册
- `POST /api/users/auth/logout/` - 登出
- `POST /api/users/auth/refresh/` - 刷新 Token

### 用户相关
- `GET /api/users/profile/` - 获取个人资料
- `PATCH /api/users/profile/` - 更新个人资料
- `POST /api/users/profile/avatar/` - 上传头像

### 文章相关
- `GET /api/articles/` - 文章列表
- `GET /api/articles/my/` - 我的文章
- `GET /api/articles/{id}/` - 文章详情
- `POST /api/articles/create/` - 创建文章
- `POST /api/articles/{id}/update/` - 更新文章
- `DELETE /api/articles/{id}/delete/` - 删除文章

### 互动相关
- `POST /api/interactions/likes/toggle/` - 点赞/取消点赞
- `POST /api/interactions/collections/toggle/` - 收藏/取消收藏
- `GET /api/interactions/notifications/` - 通知列表

## 启动项目

### 使用启动脚本
```bash
./start.sh
```

### 手动启动

**后端:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**前端:**
```bash
cd frontend
npm install
npm run dev
```

## 环境变量

### 后端 (.env)
```
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=qtribe
DB_USER=root
DB_PASSWORD=your-password
REDIS_URL=redis://127.0.0.1:6379/0
```

### 前端 (.env)
```
VITE_API_BASE_URL=http://localhost:8000/api
```

## 性能优化

### 后端
- 数据库查询优化 (select_related, prefetch_related)
- Redis 缓存
- 分页加载
- 索引优化

### 前端
- React Query 缓存
- 组件懒加载
- 图片优化
- 请求防抖/节流
