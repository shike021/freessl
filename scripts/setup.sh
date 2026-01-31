#!/bin/bash

# Free SSL Service 初始化脚本
# 用途：首次部署时的初始化设置

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# 检查是否为root用户
check_root() {
    if [ "$EUID" -ne 0 ]; then
        log_error "请使用root用户运行此脚本"
        exit 1
    fi
}

# 检查操作系统
check_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$ID
        VERSION=$VERSION_ID
        log_info "检测到操作系统: $OS $VERSION"
    else
        log_error "无法检测操作系统"
        exit 1
    fi
}

# 检查Docker是否安装
check_docker() {
    if command -v docker &> /dev/null; then
        log_info "Docker已安装: $(docker --version)"
    else
        log_warn "Docker未安装，开始安装Docker..."
        install_docker
    fi
}

# 安装Docker
install_docker() {
    log_step "安装Docker..."
    
    if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
        apt-get update
        apt-get install -y \
            ca-certificates \
            curl \
            gnupg \
            lsb-release
        
        mkdir -p /etc/apt/keyrings
        curl -fsSL https://download.docker.com/linux/$OS/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
        
        echo \
            "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/$OS \
            $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
        
        apt-get update
        apt-get install -y docker-ce docker-ce-cli containerd.io
        
        systemctl start docker
        systemctl enable docker
        
        log_info "Docker安装完成"
    elif [ "$OS" = "centos" ] || [ "$OS" = "rhel" ]; then
        yum install -y yum-utils
        yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
        yum install -y docker-ce docker-ce-cli containerd.io
        
        systemctl start docker
        systemctl enable docker
        
        log_info "Docker安装完成"
    else
        log_error "不支持的操作系统: $OS"
        exit 1
    fi
}

# 检查Docker Compose是否安装
check_docker_compose() {
    if command -v docker-compose &> /dev/null; then
        log_info "Docker Compose已安装: $(docker-compose --version)"
    else
        log_warn "Docker Compose未安装，开始安装Docker Compose..."
        install_docker_compose
    fi
}

# 安装Docker Compose
install_docker_compose() {
    log_step "安装Docker Compose..."
    
    COMPOSE_VERSION="v2.20.0"
    
    curl -L "https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" \
        -o /usr/local/bin/docker-compose
    
    chmod +x /usr/local/bin/docker-compose
    
    log_info "Docker Compose安装完成"
}

# 安装必要工具
install_tools() {
    log_step "安装必要工具..."
    
    if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
        apt-get update
        apt-get install -y git curl wget vim ufw certbot
    elif [ "$OS" = "centos" ] || [ "$OS" = "rhel" ]; then
        yum install -y git curl wget vim firewalld certbot
    fi
    
    log_info "工具安装完成"
}

# 配置防火墙
configure_firewall() {
    log_step "配置防火墙..."
    
    if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
        ufw allow 22/tcp    # SSH
        ufw allow 80/tcp    # HTTP
        ufw allow 443/tcp   # HTTPS
        ufw --force enable
        log_info "防火墙配置完成（UFW）"
    elif [ "$OS" = "centos" ] || [ "$OS" = "rhel" ]; then
        firewall-cmd --permanent --add-service=ssh
        firewall-cmd --permanent --add-service=http
        firewall-cmd --permanent --add-service=https
        firewall-cmd --reload
        log_info "防火墙配置完成（firewalld）"
    fi
}

# 创建环境变量文件
create_env_file() {
    log_step "创建环境变量文件..."
    
    if [ -f "free_ssl_service/.env" ]; then
        log_warn "环境变量文件已存在，跳过创建"
        return
    fi
    
    cp free_ssl_service/.env.sample free_ssl_service/.env
    
    # 生成随机密钥
    SECRET_KEY=$(openssl rand -hex 32)
    ENCRYPTION_KEY=$(openssl rand -base64 32)
    DB_PASSWORD=$(openssl rand -base64 16 | tr -d "=+/" | cut -c1-16)
    
    # 更新环境变量
    sed -i "s/your-secret-key-change-in-production/$SECRET_KEY/g" free_ssl_service/.env
    sed -i "s/your-encryption-key-32-bytes-long/$ENCRYPTION_KEY/g" free_ssl_service/.env
    sed -i "s/freessl_password/$DB_PASSWORD/g" free_ssl_service/.env
    
    log_info "环境变量文件创建完成"
    log_warn "请编辑 free_ssl_service/.env 文件，配置必要的环境变量"
    log_warn "特别是：EMAIL_API_KEY, ALIPAY_APP_ID, WECHAT_APP_ID 等"
}

# 创建备份目录
create_backup_dir() {
    log_step "创建备份目录..."
    
    mkdir -p /var/backups/freessl
    log_info "备份目录创建完成: /var/backups/freessl"
}

# 设置脚本执行权限
setup_scripts() {
    log_step "设置脚本执行权限..."
    
    chmod +x scripts/*.sh
    log_info "脚本执行权限设置完成"
}

# 创建日志目录
create_log_dir() {
    log_step "创建日志目录..."
    
    mkdir -p /var/log/freessl
    log_info "日志目录创建完成: /var/log/freessl"
}

# 配置定时备份
setup_cron() {
    log_step "配置定时备份..."
    
    # 添加备份任务到crontab
    (crontab -l 2>/dev/null; echo "0 2 * * * $(pwd)/scripts/backup.sh >> /var/log/freessl/backup.log 2>&1") | crontab -
    
    log_info "定时备份配置完成（每天凌晨2点）"
}

# 显示配置信息
show_config() {
    log_info "配置信息:"
    echo "----------------------------------------"
    echo "操作系统: $OS $VERSION"
    echo "Docker版本: $(docker --version)"
    echo "Docker Compose版本: $(docker-compose --version)"
    echo "项目目录: $(pwd)"
    echo "备份目录: /var/backups/freessl"
    echo "日志目录: /var/log/freessl"
    echo "----------------------------------------"
}

# 显示下一步操作
show_next_steps() {
    log_info "初始化完成！"
    echo ""
    log_info "下一步操作:"
    echo "1. 编辑环境变量文件: vim free_ssl_service/.env"
    echo "2. 配置必要的API密钥和支付信息"
    echo "3. 启动服务: docker-compose -f free_ssl_service/docker-compose.yml up -d"
    echo "4. 获取SSL证书: docker-compose exec certbot certbot certonly --webroot -w /var/www/certbot -d yourdomain.com"
    echo "5. 访问应用: http://localhost:8080"
    echo ""
    log_info "详细文档请查看 docs/ 目录"
}

# 主函数
main() {
    log_info "开始初始化Free SSL Service..."
    echo ""
    
    # 检查和安装
    check_root
    check_os
    check_docker
    check_docker_compose
    install_tools
    configure_firewall
    
    # 配置
    create_env_file
    create_backup_dir
    setup_scripts
    create_log_dir
    setup_cron
    
    # 显示信息
    show_config
    echo ""
    show_next_steps
}

# 运行主函数
main
