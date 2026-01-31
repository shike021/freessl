#!/bin/bash

# Free SSL Service 部署脚本
# 用途：自动化部署Free SSL Service到生产环境

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查是否为root用户
check_root() {
    if [ "$EUID" -ne 0 ]; then
        log_error "请使用root用户运行此脚本"
        exit 1
    fi
}

# 检查Docker是否安装
check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker未安装，请先安装Docker"
        exit 1
    fi
    log_info "Docker已安装: $(docker --version)"
}

# 检查Docker Compose是否安装
check_docker_compose() {
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose未安装，请先安装Docker Compose"
        exit 1
    fi
    log_info "Docker Compose已安装: $(docker-compose --version)"
}

# 检查环境变量文件
check_env_file() {
    if [ ! -f "free_ssl_service/.env" ]; then
        log_error "环境变量文件不存在，请先创建 free_ssl_service/.env"
        log_info "可以从 free_ssl_service/.env.sample 复制模板"
        exit 1
    fi
    log_info "环境变量文件存在"
}

# 拉取最新代码
pull_code() {
    log_info "拉取最新代码..."
    git pull origin develop
    log_info "代码拉取完成"
}

# 构建Docker镜像
build_images() {
    log_info "构建Docker镜像..."
    docker-compose -f free_ssl_service/docker-compose.yml build --no-cache
    log_info "Docker镜像构建完成"
}

# 停止旧容器
stop_containers() {
    log_info "停止旧容器..."
    docker-compose -f free_ssl_service/docker-compose.yml down
    log_info "旧容器已停止"
}

# 启动新容器
start_containers() {
    log_info "启动新容器..."
    docker-compose -f free_ssl_service/docker-compose.yml up -d
    log_info "新容器已启动"
}

# 等待服务就绪
wait_for_services() {
    log_info "等待服务启动..."
    sleep 10
    
    # 检查后端服务
    log_info "检查后端服务..."
    for i in {1..30}; do
        if curl -s http://localhost:5000 > /dev/null; then
            log_info "后端服务已就绪"
            break
        fi
        if [ $i -eq 30 ]; then
            log_error "后端服务启动超时"
            exit 1
        fi
        sleep 2
    done
    
    # 检查前端服务
    log_info "检查前端服务..."
    for i in {1..30}; do
        if curl -s http://localhost:8080 > /dev/null; then
            log_info "前端服务已就绪"
            break
        fi
        if [ $i -eq 30 ]; then
            log_error "前端服务启动超时"
            exit 1
        fi
        sleep 2
    done
}

# 初始化数据库
init_database() {
    log_info "初始化数据库..."
    docker-compose -f free_ssl_service/docker-compose.yml exec -T backend python -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('Database initialized successfully')
"
    log_info "数据库初始化完成"
}

# 清理旧镜像
cleanup_images() {
    log_info "清理未使用的Docker镜像..."
    docker image prune -f
    log_info "清理完成"
}

# 显示部署状态
show_status() {
    log_info "部署状态:"
    docker-compose -f free_ssl_service/docker-compose.yml ps
}

# 主函数
main() {
    log_info "开始部署Free SSL Service..."
    
    # 检查环境
    check_root
    check_docker
    check_docker_compose
    check_env_file
    
    # 部署步骤
    pull_code
    stop_containers
    build_images
    start_containers
    wait_for_services
    init_database
    cleanup_images
    
    # 显示状态
    show_status
    
    log_info "部署完成！"
    log_info "前端访问地址: http://localhost:8080"
    log_info "后端API地址: http://localhost:5000"
    log_info "API文档地址: http://localhost:5000/apidocs"
}

# 运行主函数
main
