# QTribe - 博客社交平台

前后端分离架构的博客社交平台项目。

## 项目结构

```
.
├── QTribe_api/          # 后端 API (Django REST Framework)
│   ├── QTribe_api/      # 项目配置
│   ├── apps/            # 应用模块
│   │   ├── user/        # 用户模块
│   │   ├── pieces_info/ # 内容模块
│   │   └── verify_code/ # 验证码模块
│   ├── middleware/      # 中间件
│   ├── manage.py
│   └── requirements.txt
│
├── qtribe-web/          # 前端 (React + TypeScript)
│   ├── src/
│   │   ├── api/         # API 请求
│   │   ├── components/  # 组件
│   │   ├── lib/         # 工具库
│   │   ├── pages/       # 页面
│   │   ├── stores/      # 状态管理
│   │   └── types/       # TypeScript 类型
│   ├── package.json
│   └── vite.config.ts
│
└── media/               # 媒体文件
```

## 技术栈

### 后端
- Django 4.2
- Django REST Framework
- JWT 认证 (djangorestframework-simplejwt)
- MySQL
- Redis
- CORS 支持

### 前端
- React 18
- TypeScript (严格模式)
- Vite
- Tailwind CSS
- React Query
- Zustand (状态管理)
- React Router v6
- React Hook Form + Zod (表单验证)

## 快速开始

### 后端启动

```bash
cd QTribe_api

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 启动开发服务器
python manage.py runserver
```

### 前端启动

```bash
cd qtribe-web

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

## API 文档

### 认证 API
- `POST /api/v1/auth/register/` - 用户注册
- `POST /api/v1/auth/login/` - 用户登录
- `POST /api/v1/auth/logout/` - 用户登出
- `POST /api/v1/auth/token/refresh/` - 刷新 Token
- `GET /api/v1/auth/profile/` - 获取用户信息
- `PATCH /api/v1/auth/profile/` - 更新用户信息
- `POST /api/v1/auth/profile/password/` - 修改密码
- `POST /api/v1/auth/profile/avatar/` - 上传头像

### 文章 API
- `GET /api/v1/articles/` - 文章列表
- `POST /api/v1/articles/` - 创建文章
- `GET /api/v1/articles/{id}/` - 文章详情
- `PUT /api/v1/articles/{id}/` - 更新文章
- `DELETE /api/v1/articles/{id}/` - 删除文章
- `POST /api/v1/articles/{id}/star/` - 点赞/取消点赞
- `POST /api/v1/articles/{id}/collect/` - 收藏/取消收藏
- `POST /api/v1/articles/{id}/top/` - 置顶/取消置顶

### 视频 API
- `GET /api/v1/videos/` - 视频列表
- `POST /api/v1/videos/` - 上传视频
- `GET /api/v1/videos/{id}/` - 视频详情
- `PUT /api/v1/videos/{id}/` - 更新视频
- `DELETE /api/v1/videos/{id}/` - 删除视频
- `POST /api/v1/videos/{id}/star/` - 点赞/取消点赞
- `POST /api/v1/videos/{id}/collect/` - 收藏/取消收藏

### 评论 API
- `GET /api/v1/comments/` - 评论列表
- `POST /api/v1/comments/` - 发表评论
- `DELETE /api/v1/comments/{id}/` - 删除评论

### 消息 API
- `GET /api/v1/messages/` - 消息列表
- `POST /api/v1/messages/read-all/` - 全部标记已读
- `GET /api/v1/messages/unread-count/` - 未读消息数

## 安全特性

- JWT Token 认证
- XSS 防护中间件
- 请求频率限制
- CORS 配置
- 密码强度验证

## 环境变量

### 后端
```
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=qtribe
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=3306
REDIS_HOST=localhost
```

### 前端
```
VITE_API_BASE_URL=/api/v1
```

## License

MIT
