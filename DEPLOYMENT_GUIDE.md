# FreeSSL 项目 Ubuntu 部署操作手册

## 一、环境信息

| 项目 | 值 |
|------|-----|
| 公网IP | 103.47.83.234 |
| CPU | 4核 |
| 内存 | 8GB |
| 磁盘剩余 | 50GB |
| Docker版本 | 29.3.0 |
| Docker Compose版本 | 5.1.0 |

### 现有服务端口占用

| 端口 | 服务 | 状态 |
|------|------|------|
| 80/443 | 宿主机Nginx | 已被占用 |
| 3309 | 宿主机MariaDB | 已被占用 |
| 8864 | 其他服务 | 已被占用 |

### 部署架构

```
                    ┌─────────────────────────────────────┐
                    │         宿主机 Nginx (80/443)        │
                    │   freessl.shi021.cn 反向代理         │
                    └──────────────┬──────────────────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                    │
              ▼                    ▼                    ▼
    ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
    │   frontend      │  │   backend       │  │   mariadb       │
    │   (8081:8080)   │  │   (5001:5000)   │  │   (3310:3306)   │
    │   Vue 3 + Nginx │  │   Flask API     │  │   数据库        │
    └─────────────────┘  └─────────────────┘  └─────────────────┘
                                 │                    │
                                 ▼                    │
                      ┌─────────────────┐              │
                      │   redis         │              │
                      │   (6380:6379)   │              │
                      └─────────────────┘              │
                                 │                     │
                                 ▼                     │
                      ┌─────────────────┐              │
                      │  celery-worker  │──────────────┘
                      │  celery-beat    │
                      └─────────────────┘
```

## 二、部署文件说明

| 文件 | 说明 |
|------|------|
| `docker-compose.ubuntu.yml` | Ubuntu专用部署配置（不使用nginx/certbot容器） |
| `config/nginx/freessl.shi021.cn.conf` | 宿主机Nginx配置文件 |
| `.env.ubuntu` | Ubuntu部署环境变量模板 |

## 三、部署步骤

### 步骤1：克隆项目到Ubuntu服务器

```bash
# 在Ubuntu服务器上执行
cd /home/ubuntu
git clone <项目仓库地址> freessl
cd freessl/free_ssl_service
```

### 步骤2：复制并配置环境变量

```bash
# 复制环境变量文件
cp .env.ubuntu .env

# 生成并设置SECRET_KEY
# 在本地执行后复制，或在服务器上执行：
python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))"
# 将输出添加到.env文件

# 生成ENCRYPTION_KEY
python -c "from cryptography.fernet import Fernet; print('ENCRYPTION_KEY=' + Fernet.generate_key().decode())"
# 将输出添加到.env文件

# 编辑环境变量
nano .env
```

**必须修改的值**：
```env
SECRET_KEY=<填入生成的32字节随机字符串>
ENCRYPTION_KEY=<填入生成的Fernet密钥>
MARIADB_PASS=<数据库密码，建议修改>
EMAIL_API_KEY=<你的SendGrid API密钥>
```

### 步骤3：配置宿主机Nginx

```bash
# 复制Nginx配置文件
sudo cp config/nginx/freessl.shi021.cn.conf /etc/nginx/sites-available/freessl.shi021.cn

# 创建符号链接
sudo ln -s /etc/nginx/sites-available/freessl.shi021.cn /etc/nginx/sites-enabled/

# 测试Nginx配置
sudo nginx -t

# 重启Nginx
sudo systemctl restart nginx
```

### 步骤4：构建并启动服务

```bash
# 构建所有镜像（可能需要10-20分钟）
docker compose -f docker-compose.ubuntu.yml build

# 启动所有服务
docker compose -f docker-compose.ubuntu.yml up -d

# 查看服务状态
docker compose -f docker-compose.ubuntu.yml ps
```

### 步骤5：初始化数据库

```bash
# 等待几秒让服务完全启动
sleep 10

# 初始化数据库表
docker compose -f docker-compose.ubuntu.yml exec backend python -c "from models.db import db; from app import app; with app.app_context(): db.create_all()"
```

### 步骤6：验证部署

```bash
# 检查所有容器状态
docker compose -f docker-compose.ubuntu.yml ps

# 查看日志
docker compose -f docker-compose.ubuntu.yml logs -f

# 测试API健康检查
curl http://localhost:5001/health

# 测试前端
curl http://localhost:8081
```

### 步骤7：访问网站

在浏览器中访问：`https://freessl.shi021.cn`

## 四、服务管理命令

### 启动/停止/重启

```bash
# 停止所有服务
docker compose -f docker-compose.ubuntu.yml down

# 启动所有服务
docker compose -f docker-compose.ubuntu.yml up -d

# 重启所有服务
docker compose -f docker-compose.ubuntu.yml restart

# 重启特定服务
docker compose -f docker-compose.ubuntu.yml restart backend
```

### 查看日志

```bash
# 查看所有服务日志
docker compose -f docker-compose.ubuntu.yml logs -f

# 查看特定服务日志
docker compose -f docker-compose.ubuntu.yml logs -f backend
docker compose -f docker-compose.ubuntu.yml logs -f frontend

# 查看最近100行日志
docker compose -f docker-compose.ubuntu.yml logs --tail 100
```

### 进入容器

```bash
# 进入backend容器
docker compose -f docker-compose.ubuntu.yml exec backend sh

# 进入mariadb容器
docker compose -f docker-compose.ubuntu.yml exec mariadb mysql -u freessl -p
```

## 五、端口说明

| 容器内端口 | 宿主机端口 | 服务 | 访问方式 |
|-----------|-----------|------|---------|
| 8080 | 8081 | frontend | 通过Nginx代理 |
| 5000 | 5001 | backend | 通过Nginx代理 |
| 3306 | 3310 | mariadb | 仅容器间访问 |
| 6379 | 6380 | redis | 仅容器间访问 |

## 六、数据备份

### 备份数据库

```bash
# 创建备份目录
mkdir -p backups

# 备份数据库
docker compose -f docker-compose.ubuntu.yml exec mariadb mysqldump -u freessl -pfreessl_password freessl > backups/freessl_$(date +%Y%m%d).sql

# 恢复数据库
docker compose -f docker-compose.ubuntu.yml exec -T mariadb mysql -u freessl -pfreessl_password freessl < backups/freessl_20240101.sql
```

### 备份配置

```bash
# 备份.env文件（包含敏感信息，请妥善保管）
cp .env backups/.env.backup
```

## 七、故障排查

### 常见问题

| 问题 | 可能原因 | 解决方案 |
|------|---------|---------|
| 容器无法启动 | 端口冲突 | 检查端口占用：`sudo netstat -tulpn \| grep LISTEN` |
| 数据库连接失败 | 环境变量未设置 | 检查.env文件是否正确配置 |
| 前端无法访问 | Nginx未正确配置 | 检查Nginx配置和日志 |
| API返回500错误 | backend异常 | 查看backend日志 |

### 检查服务状态

```bash
# 查看所有容器
docker ps -a

# 查看容器日志
docker compose -f docker-compose.ubuntu.yml logs backend

# 检查端口占用
sudo netstat -tulpn | grep LISTEN

# 检查Nginx状态
sudo systemctl status nginx

# 检查Nginx错误日志
sudo tail -f /var/log/nginx/error.log
```

### 重建服务

```bash
# 停止并删除容器
docker compose -f docker-compose.ubuntu.yml down

# 删除镜像（可选）
docker compose -f docker-compose.ubuntu.yml down --rmi local

# 重新构建并启动
docker compose -f docker-compose.ubuntu.yml up -d --build
```

## 八、更新部署

```bash
# 拉取最新代码
git pull origin develop

# 重新构建（如果Dockerfile有变化）
docker compose -f docker-compose.ubuntu.yml build

# 重启服务
docker compose -f docker-compose.ubuntu.yml up -d
```

## 九、资源限制

当前配置的资源限制（可在docker-compose.ubuntu.yml中调整）：

| 服务 | CPU限制 | 内存限制 |
|------|--------|---------|
| frontend | 0.5核 | 512MB |
| backend | 1核 | 1GB |
| mariadb | 0.5核 | 512MB |
| redis | 0.25核 | 256MB |
| celery-worker | 0.5核 | 512MB |
| celery-beat | 0.25核 | 256MB |

**总计**：约2.5核CPU，约2.5GB内存

## 十、安全建议

1. **修改默认密码**：立即修改.env中的所有密码
2. **启用防火墙**：只开放80/443端口
   ```bash
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```
3. **定期备份**：建立定期备份机制
4. **更新依赖**：定期更新Docker镜像和系统包