#!/bin/bash

# QTribe 启动脚本
# 用于同时启动前端和后端开发服务器

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=================================${NC}"
echo -e "${GREEN}    QTribe 博客社交平台启动脚本    ${NC}"
echo -e "${GREEN}=================================${NC}"
echo ""

# 检查是否安装了必要的依赖
check_dependencies() {
    echo -e "${YELLOW}检查依赖...${NC}"

    # 检查 Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}错误: 未安装 Python3${NC}"
        exit 1
    fi

    # 检查 Node.js
    if ! command -v node &> /dev/null; then
        echo -e "${RED}错误: 未安装 Node.js${NC}"
        exit 1
    fi

    # 检查 Redis
    if ! command -v redis-cli &> /dev/null; then
        echo -e "${YELLOW}警告: 未安装 Redis，缓存功能可能无法使用${NC}"
    fi

    echo -e "${GREEN}依赖检查完成${NC}"
    echo ""
}

# 启动后端
start_backend() {
    echo -e "${YELLOW}启动后端服务...${NC}"
    cd backend

    # 检查虚拟环境
    if [ ! -d "venv" ]; then
        echo -e "${YELLOW}创建 Python 虚拟环境...${NC}"
        python3 -m venv venv
    fi

    # 激活虚拟环境
    source venv/bin/activate

    # 升级 pip
    echo -e "${YELLOW}升级 pip...${NC}"
    pip install --upgrade pip setuptools wheel

    # 安装依赖
    echo -e "${YELLOW}安装后端依赖...${NC}"
    pip install -r requirements.txt

    # 检查 .env 文件
    if [ ! -f ".env" ]; then
        echo -e "${YELLOW}创建 .env 文件...${NC}"
        cp .env.example .env
        echo -e "${YELLOW}请编辑 backend/.env 文件配置数据库等信息${NC}"
    fi

    # 运行迁移
    echo -e "${YELLOW}运行数据库迁移...${NC}"
    python manage.py migrate

    # 启动开发服务器
    echo -e "${GREEN}后端服务启动在 http://localhost:8000${NC}"
    python manage.py runserver 0.0.0.0:8000 &
    BACKEND_PID=$!

    cd ..
}

# 启动前端
start_frontend() {
    echo -e "${YELLOW}启动前端服务...${NC}"
    cd frontend

    # 检查 .env 文件
    if [ ! -f ".env" ]; then
        echo -e "${YELLOW}创建 .env 文件...${NC}"
        cp .env.example .env
    fi

    # 安装依赖
    echo -e "${YELLOW}安装前端依赖...${NC}"
    npm install

    # 启动开发服务器
    echo -e "${GREEN}前端服务启动在 http://localhost:5173${NC}"
    npm run dev &
    FRONTEND_PID=$!

    cd ..
}

# 清理函数
cleanup() {
    echo ""
    echo -e "${YELLOW}正在关闭服务...${NC}"
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
    fi
    echo -e "${GREEN}服务已关闭${NC}"
    exit 0
}

# 捕获中断信号
trap cleanup INT TERM

# 主程序
main() {
    check_dependencies

    # 启动服务
    start_backend
    start_frontend

    echo ""
    echo -e "${GREEN}=================================${NC}"
    echo -e "${GREEN}    所有服务已启动!              ${NC}"
    echo -e "${GREEN}=================================${NC}"
    echo ""
    echo -e "后端 API: ${GREEN}http://localhost:8000${NC}"
    echo -e "前端页面: ${GREEN}http://localhost:5173${NC}"
    echo ""
    echo -e "按 ${YELLOW}Ctrl+C${NC} 停止所有服务"
    echo ""

    # 等待用户中断
    wait
}

main
