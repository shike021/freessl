#!/bin/bash

# Free SSL Service 备份脚本
# 用途：备份数据库、证书和配置文件

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

# 配置
BACKUP_DIR="/var/backups/freessl"
RETENTION_DAYS=30
DATE=$(date +%Y%m%d_%H%M%S)

# 创建备份目录
create_backup_dir() {
    if [ ! -d "$BACKUP_DIR" ]; then
        mkdir -p "$BACKUP_DIR"
        log_info "创建备份目录: $BACKUP_DIR"
    fi
}

# 备份数据库
backup_database() {
    log_info "备份数据库..."
    
    # 读取数据库密码
    source free_ssl_service/.env
    DB_PASS=$MARIADB_PASS
    
    # 备份数据库
    docker-compose -f free_ssl_service/docker-compose.yml exec -T mariadb mysqldump \
        -u freessl -p"$DB_PASS" \
        --single-transaction \
        --routines \
        --triggers \
        freessl > "$BACKUP_DIR/db_$DATE.sql"
    
    # 压缩备份
    gzip "$BACKUP_DIR/db_$DATE.sql"
    
    log_info "数据库备份完成: $BACKUP_DIR/db_$DATE.sql.gz"
}

# 备份证书
backup_certificates() {
    log_info "备份证书..."
    
    # 备份Let's Encrypt证书
    docker run --rm \
        -v freessl_certbot-config:/data \
        -v "$BACKUP_DIR":/backup \
        alpine tar czf "/backup/certbot_$DATE.tar.gz" -C /data .
    
    log_info "证书备份完成: $BACKUP_DIR/certbot_$DATE.tar.gz"
}

# 备份配置文件
backup_config() {
    log_info "备份配置文件..."
    
    # 备份环境变量文件
    cp free_ssl_service/.env "$BACKUP_DIR/env_$DATE"
    
    # 备份Nginx配置
    cp free_ssl_service/nginx/nginx.conf "$BACKUP_DIR/nginx_$DATE.conf"
    
    # 备份Docker Compose配置
    cp free_ssl_service/docker-compose.yml "$BACKUP_DIR/docker-compose_$DATE.yml"
    
    log_info "配置文件备份完成"
}

# 备份上传的文件（如果有）
backup_uploads() {
    log_info "备份上传的文件..."
    
    # 如果有上传文件目录，备份它
    if [ -d "free_ssl_service/uploads" ]; then
        tar czf "$BACKUP_DIR/uploads_$DATE.tar.gz" -C free_ssl_service uploads
        log_info "上传文件备份完成: $BACKUP_DIR/uploads_$DATE.tar.gz"
    else
        log_warn "没有上传文件目录，跳过"
    fi
}

# 清理旧备份
cleanup_old_backups() {
    log_info "清理 $RETENTION_DAYS 天前的备份..."
    
    # 删除旧的数据库备份
    find "$BACKUP_DIR" -name "db_*.sql.gz" -mtime +$RETENTION_DAYS -delete
    
    # 删除旧的证书备份
    find "$BACKUP_DIR" -name "certbot_*.tar.gz" -mtime +$RETENTION_DAYS -delete
    
    # 删除旧的配置备份
    find "$BACKUP_DIR" -name "env_*" -mtime +$RETENTION_DAYS -delete
    find "$BACKUP_DIR" -name "nginx_*.conf" -mtime +$RETENTION_DAYS -delete
    find "$BACKUP_DIR" -name "docker-compose_*.yml" -mtime +$RETENTION_DAYS -delete
    
    # 删除旧的上传文件备份
    find "$BACKUP_DIR" -name "uploads_*.tar.gz" -mtime +$RETENTION_DAYS -delete
    
    log_info "旧备份清理完成"
}

# 显示备份信息
show_backup_info() {
    log_info "备份信息:"
    log_info "备份目录: $BACKUP_DIR"
    log_info "备份日期: $DATE"
    log_info "保留天数: $RETENTION_DAYS"
    
    # 显示备份文件大小
    log_info "备份文件:"
    ls -lh "$BACKUP_DIR"/*_$DATE* 2>/dev/null || log_warn "没有找到备份文件"
    
    # 显示磁盘使用情况
    log_info "备份目录磁盘使用:"
    du -sh "$BACKUP_DIR"
}

# 发送备份通知（可选）
send_notification() {
    # 如果配置了邮件通知，可以在这里发送通知
    # 例如：使用SendGrid或其他邮件服务
    log_info "备份通知功能未配置，跳过"
}

# 主函数
main() {
    log_info "开始备份Free SSL Service..."
    
    # 执行备份
    create_backup_dir
    backup_database
    backup_certificates
    backup_config
    backup_uploads
    cleanup_old_backups
    
    # 显示信息
    show_backup_info
    
    # 发送通知
    send_notification
    
    log_info "备份完成！"
}

# 运行主函数
main
