# 部署文档

## 概述

本文档详细说明如何将Free SSL Service部署到生产环境。

## 系统要求

### 硬件要求
- CPU: 2核或以上
- 内存: 4GB或以上
- 硬盘: 20GB或以上

### 软件要求
- 操作系统: Ubuntu 20.04+ / CentOS 8+ / Debian 11+
- Docker: 20.10+
- Docker Compose: 1.29+
- Nginx: 1.18+ (可选，用于反向代理)
- 域名: 已解析到服务器IP

## 部署步骤

### 1. 准备服务器

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装必要工具
sudo apt install -y curl wget git vim ufw

# 配置防火墙
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### 2. 安装Docker和Docker Compose

```bash
# 安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 启动Docker服务
sudo systemctl start docker
sudo systemctl enable docker

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 验证安装
docker --version
docker-compose --version
```

### 3. 克隆代码

```bash
# 克隆仓库
git clone https://github.com/yourrepo/free-ssl-service.git
cd free-ssl-service

# 切换到生产分支（如果存在）
git checkout production
```

### 4. 配置环境变量

```bash
# 复制环境变量模板
cp free_ssl_service/.env.sample free_ssl_service/.env

# 编辑环境变量
vim free_ssl_service/.env
```

**生产环境必须修改的变量**：

```bash
# 数据库密码（必须修改）
MARIADB_PASS=<strong-password>

# Flask密钥（必须修改为随机字符串）
SECRET_KEY=<random-secret-key>

# 加密密钥（必须是32字节）
ENCRYPTION_KEY=<32-byte-encryption-key>

# SendGrid API密钥
EMAIL_API_KEY=<your-sendgrid-api-key>

# 发件人邮箱
EMAIL_FROM=<your-email>

# 支付宝配置
ALIPAY_APP_ID=<your-alipay-app-id>
ALIPAY_PRIVATE_KEY=<your-alipay-private-key>
ALIPAY_PUBLIC_KEY=<your-alipay-public-key>

# 微信支付配置
WECHAT_APP_ID=<your-wechat-app-id>
WECHAT_MCH_ID=<your-wechat-mch-id>
WECHAT_API_KEY=<your-wechat-api-key>
```

### 5. 配置Nginx

如果使用外部Nginx作为反向代理：

```bash
# 安装Nginx
sudo apt install -y nginx

# 创建站点配置
sudo vim /etc/nginx/sites-available/freessl
```

Nginx配置示例：

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /apidocs {
        proxy_pass http://localhost:5000/apidocs;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

启用站点：

```bash
sudo ln -s /etc/nginx/sites-available/freessl /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 6. 获取SSL证书

```bash
# 安装Certbot
sudo apt install -y certbot python3-certbot-nginx

# 获取SSL证书（使用Nginx插件）
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# 证书会自动配置到Nginx
```

如果使用Docker内的Nginx：

```bash
# 启动服务
docker-compose -f free_ssl_service/docker-compose.yml up -d

# 获取证书
docker-compose exec certbot certbot certonly --webroot -w /var/www/certbot -d yourdomain.com -d www.yourdomain.com

# 重启Nginx
docker-compose restart nginx
```

### 7. 启动服务

```bash
# 构建并启动所有服务
docker-compose -f free_ssl_service/docker-compose.yml up -d --build

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 8. 验证部署

```bash
# 检查前端
curl -I http://yourdomain.com

# 检查后端API
curl http://yourdomain.com/api/health

# 检查HTTPS
curl -I https://yourdomain.com
```

## 数据库初始化

首次启动后，需要初始化数据库：

```bash
# 进入后端容器
docker-compose exec backend sh

# 初始化数据库
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# 退出容器
exit
```

## 备份策略

### 数据库备份

创建备份脚本 `scripts/backup.sh`：

```bash
#!/bin/bash

# 备份目录
BACKUP_DIR="/var/backups/freessl"
DATE=$(date +%Y%m%d_%H%M%S)

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份数据库
docker-compose exec -T mariadb mysqldump -u freessl -p$MARIADB_PASS freessl > $BACKUP_DIR/db_$DATE.sql

# 压缩备份
gzip $BACKUP_DIR/db_$DATE.sql

# 删除30天前的备份
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +30 -delete

echo "Backup completed: $BACKUP_DIR/db_$DATE.sql.gz"
```

设置定时备份：

```bash
# 添加到crontab
crontab -e

# 每天凌晨2点备份
0 2 * * * /path/to/scripts/backup.sh
```

### 证书备份

```bash
# 备份证书
docker run --rm -v freessl_certbot-config:/data -v $(pwd):/backup alpine tar czf /backup/certbot-backup-$(date +%Y%m%d).tar.gz -C /data .
```

## 监控

### 查看服务状态

```bash
# 查看所有容器状态
docker-compose ps

# 查看资源使用情况
docker stats

# 查看日志
docker-compose logs -f --tail=100
```

### 健康检查

创建健康检查脚本 `scripts/health-check.sh`：

```bash
#!/bin/bash

# 检查前端
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080)
if [ $FRONTEND_STATUS -eq 200 ]; then
    echo "Frontend: OK"
else
    echo "Frontend: FAILED ($FRONTEND_STATUS)"
fi

# 检查后端
BACKEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/api/health)
if [ $BACKEND_STATUS -eq 200 ]; then
    echo "Backend: OK"
else
    echo "Backend: FAILED ($BACKEND_STATUS)"
fi

# 检查数据库
DB_STATUS=$(docker-compose exec -T mariadb mysqladmin -u freessl -p$MARIADB_PASS ping 2>&1)
if [[ $DB_STATUS == *"mysqld is alive"* ]]; then
    echo "Database: OK"
else
    echo "Database: FAILED"
fi
```

## 更新部署

### 拉取最新代码

```bash
cd /path/to/free-ssl-service
git pull origin production
```

### 重新构建和部署

```bash
# 停止服务
docker-compose down

# 重新构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 清理旧镜像
docker image prune -f
```

### 数据库迁移

如果有数据库结构变更：

```bash
# 进入后端容器
docker-compose exec backend sh

# 运行迁移（需要配置Flask-Migrate）
flask db upgrade

# 退出容器
exit
```

## 故障排查

### 容器无法启动

```bash
# 查看容器日志
docker-compose logs <service-name>

# 检查端口占用
netstat -tlnp | grep -E ':(80|443|5000|3306|6379)'

# 检查磁盘空间
df -h

# 检查内存使用
free -h
```

### 数据库连接失败

```bash
# 检查MariaDB容器状态
docker-compose ps mariadb

# 进入MariaDB容器
docker-compose exec mariadb mysql -u freessl -p

# 检查数据库
SHOW DATABASES;
USE freessl;
SHOW TABLES;
```

### SSL证书问题

```bash
# 手动续期证书
docker-compose exec certbot certbot renew

# 检查证书有效期
docker-compose exec certbot certbot certificates

# 重新加载Nginx
docker-compose restart nginx
```

## 性能优化

### 数据库优化

编辑 `free_ssl_service/docker-compose.yml`，调整MariaDB配置：

```yaml
mariadb:
  image: mariadb:10.6
  command: --innodb-buffer-pool-size=1G --max-connections=200
  environment:
    - MYSQL_ROOT_PASSWORD=root_password
    - MYSQL_DATABASE=freessl
    - MYSQL_USER=freessl
    - MYSQL_PASSWORD=freessl_password
  volumes:
    - mariadb-data:/var/lib/mysql
```

### Redis优化

```yaml
redis:
  image: redis:7-alpine
  command: redis-server --maxmemory 512mb --maxmemory-policy allkeys-lru
```

### Nginx优化

编辑 `nginx/nginx.conf`：

```nginx
worker_processes auto;
worker_connections 2048;
keepalive_timeout 65;
client_max_body_size 10M;
```

## 安全加固

1. **使用强密码**：所有密码至少16位，包含大小写字母、数字和特殊字符
2. **定期更新**：及时更新系统和Docker镜像
3. **限制访问**：使用防火墙限制不必要的端口访问
4. **监控日志**：定期检查日志文件，发现异常及时处理
5. **备份数据**：定期备份数据库和证书
6. **使用HTTPS**：确保所有通信都使用HTTPS加密

## 支持

如有问题，请查看 [故障排查文档](troubleshooting.md) 或提交 [Issue](https://github.com/yourrepo/free-ssl-service/issues)。
