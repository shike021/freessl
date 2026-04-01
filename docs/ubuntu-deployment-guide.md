# Ubuntu 服务器部署指南

## 服务器信息

- **域名**: freessl.shi021.cn
- **系统**: Ubuntu 20.04+ / 22.04

## 部署前准备

### 1. 确认域名解析

```bash
# 检查域名是否已解析到服务器 IP
ping freessl.shi021.cn
nslookup freessl.shi021.cn
```

### 2. 安装 Docker 和 Docker Compose

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装必要工具
sudo apt install -y curl wget git vim ufw apt-transport-https ca-certificates gnupg lsb-release

# 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 将当前用户加入 docker 组
sudo usermod -aG docker $USER

# 安装 Docker Compose (v2)
DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
mkdir -p $DOCKER_CONFIG/cli-plugins
curl -SL https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose
chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose

# 验证安装
docker --version
docker compose version
```

### 3. 配置防火墙

```bash
# 配置 UFW 防火墙
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
sudo ufw status
```

## 部署步骤

### 1. 克隆代码

```bash
cd ~
git clone <your-repo-url> freessl
cd freessl
```

### 2. 创建环境变量文件

```bash
cd ~/freessl/free_ssl_service

# 复制环境变量模板
cp .env.sample .env

# 编辑环境变量
vim .env
```

### 3. 配置环境变量 (.env)

```bash
# ===== 数据库配置 (必须修改) =====
MARIADB_HOST=mariadb
MARIADB_PORT=3306
MARIADB_USER=freessl
MARIADB_PASS=YourStrongPassword123!        # 修改为强密码
MARIADB_DB=freessl
MYSQL_ROOT_PASSWORD=YourRootPassword456!   # 修改为强密码

# ===== 安全密钥 (必须修改) =====
SECRET_KEY=your-random-secret-key-at-least-32-characters  # 生成随机字符串
ENCRYPTION_KEY=your-32-byte-encryption-key                # 必须 32 字节

# 生成随机密钥示例:
# python3 -c "import secrets; print(secrets.token_hex(32))"

# ===== 邮件配置 (SendGrid) =====
EMAIL_SERVICE=sendgrid
EMAIL_API_KEY=your-sendgrid-api-key
EMAIL_FROM=noreply@freessl.shi021.cn

# ===== Celery/Redis 配置 (默认即可) =====
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# ===== OAuth 配置 (可选) =====
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
WECHAT_CLIENT_ID=
WECHAT_CLIENT_SECRET=
```

### 4. 获取 SSL 证书

**方法一：首次部署时使用 standalone 模式**

```bash
# 停止可能占用 80 端口的服务
sudo systemctl stop apache2 2>/dev/null || true
sudo systemctl stop nginx 2>/dev/null || true

# 使用 Docker 运行 Certbot 获取证书
sudo docker run --rm -it \
    -v freessl_certbot-config:/etc/letsencrypt \
    -v freessl_certbot-www:/var/www/certbot \
    certbot/certbot certonly --webroot \
    -w /var/www/certbot \
    -d freessl.shi021.cn \
    -d www.freessl.shi021.cn \
    --email your-email@example.com \
    --agree-tos \
    --non-interactive
```

**方法二：如果已有证书**

跳过此步骤，确保证书位于正确 volume 中。

### 5. 启动服务

```bash
cd ~/freessl

# 使用生产配置启动
docker compose -f free_ssl_service/docker-compose.prod.yml up -d --build

# 查看服务状态
docker compose ps

# 查看日志
docker compose logs -f
```

### 6. 验证部署

```bash
# 检查前端
curl -I http://freessl.shi021.cn

# 检查后端 API
curl http://localhost:5000/api/health 2>/dev/null || echo "Backend not directly accessible"

# 检查 HTTPS
curl -I https://freessl.shi021.cn

# 检查 Swagger 文档
curl https://freessl.shi021.cn/apidocs
```

## 初始化数据库

首次部署后初始化数据库：

```bash
cd ~/freessl
docker compose -f free_ssl_service/docker-compose.prod.yml exec backend python -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('Database initialized successfully')
"
```

## 常用运维命令

### 查看服务状态

```bash
# 查看所有容器状态
docker compose -f free_ssl_service/docker-compose.prod.yml ps

# 查看资源使用情况
docker stats
```

### 查看日志

```bash
# 查看所有服务日志
docker compose logs -f

# 查看特定服务日志
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f celery-worker
docker compose logs -f nginx
```

### 重启服务

```bash
# 重启所有服务
docker compose restart

# 重启特定服务
docker compose restart backend
docker compose restart nginx
```

### 更新部署

```bash
cd ~/freessl

# 拉取最新代码
git pull

# 重新构建并启动
docker compose -f free_ssl_service/docker-compose.prod.yml up -d --build

# 清理旧镜像
docker image prune -f
```

### 备份数据

```bash
# 备份数据库
cd ~/freessl
mkdir -p ~/backups
docker compose exec -T mariadb mysqldump -u root -p${MYSQL_ROOT_PASSWORD} freessl > ~/backups/db_backup_$(date +%Y%m%d_%H%M%S).sql

# 备份证书
docker run --rm \
    -v freessl_certbot-config:/data \
    -v ~/backups:/backup \
    alpine tar czf /backup/certbot_backup_$(date +%Y%m%d).tar.gz -C /data .
```

### 证书续期

```bash
# 手动续期证书
docker compose exec certbot certbot renew --force-renewal

# 检查证书有效期
docker compose exec certbot certbot certificates
```

## 故障排查

### 容器无法启动

```bash
# 查看容器日志
docker compose logs backend

# 检查端口占用
sudo netstat -tlnp | grep -E ':(80|443|5000|3306|6379)'

# 检查磁盘空间
df -h

# 检查内存使用
free -h
```

### 数据库连接失败

```bash
# 检查 MariaDB 容器
docker compose ps mariadb

# 查看 MariaDB 日志
docker compose logs mariadb

# 进入 MariaDB 容器
docker compose exec mariadb mysql -u root -p
```

### HTTPS 无法访问

```bash
# 检查证书是否存在
docker compose run --rm certbot ls /etc/letsencrypt/live/

# 检查 Nginx 配置
docker compose exec nginx nginx -t

# 重启 Nginx
docker compose restart nginx
```

### 证书域名不匹配

如果证书域名是 localhost 而不是 freessl.shi021.cn：

```bash
# 删除旧证书
docker volume rm freessl_certbot-config

# 重新获取证书
docker compose run --rm certbot certonly --webroot \
    -w /var/www/certbot \
    -d freessl.shi021.cn \
    -d www.freessl.shi021.cn \
    --email your-email@example.com

# 重启 Nginx
docker compose restart nginx
```

## 安全加固建议

1. **定期更新系统**: `sudo apt update && sudo apt upgrade -y`
2. **定期备份数据**: 设置 cron 定时备份
3. **监控日志**: 使用 `fail2ban` 防止暴力破解
4. **限制 SSH 访问**: 使用密钥登录，禁用密码登录
5. **定期轮换密钥**: 定期更换 `.env` 中的密钥和密码

## 监控和告警

建议配置：
- Uptime 监控（如 UptimeRobot）
- 服务器资源监控（如 Netdata）
- 证书到期提醒（已内置，到期前 30 天邮件通知）

## 联系支持

如有问题，请查看项目文档或提交 Issue。
