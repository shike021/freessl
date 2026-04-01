# Docker 配置文件检查清单

## 已修复的问题

### 1. nginx.conf
- [x] `server_name` 从 `localhost` 改为 `freessl.shi021.cn`
- [x] SSL 证书路径从 `/etc/letsencrypt/live/localhost/` 改为 `/etc/letsencrypt/live/freessl.shi021.cn/`
- [x] 添加 `/health` 端点用于健康检查

### 2. docker-compose.prod.yml
- [x] 前端 `expose` 从 `"80"` 改为 `"8080"`（与 Dockerfile 一致）
- [x] `VUE_APP_API_URL` 从 `yourdomain.com` 改为 `freessl.shi021.cn`
- [x] 移除不必要的 `args` 配置

### 3. backend/Dockerfile
- [x] 移除 PyPI 镜像源（`-i https://pypi.tuna.tsinghua.edu.cn/simple`），使用官方源

### 4. frontend/Dockerfile
- [x] 移除华为镜像源，使用官方 `node:22-alpine` 和 `nginx:1.25-alpine`

## 部署前检查清单

### 远端服务器准备

```bash
# 1. 确认域名解析
ping freessl.shi021.cn
# 应该解析到你的服务器 IP

# 2. 确认 Docker 安装
docker --version
docker compose version

# 3. 确认防火墙开放
sudo ufw status
# 应该开放 22, 80, 443 端口
```

### 环境变量检查

在服务器上运行：

```bash
cd ~/freessl/free_ssl_service
cat .env
```

确认以下变量已正确设置：

- [ ] `MARIADB_PASS` - 数据库密码（强密码）
- [ ] `MYSQL_ROOT_PASSWORD` - MariaDB root 密码（强密码）
- [ ] `SECRET_KEY` - Flask 密钥（随机字符串）
- [ ] `ENCRYPTION_KEY` - 加密密钥（32 字节）
- [ ] `EMAIL_API_KEY` - SendGrid API 密钥

### SSL 证书检查

```bash
# 检查证书是否已获取
docker volume inspect freessl_certbot-config

# 检查证书文件
docker run --rm -v freessl_certbot-config:/data alpine ls -la /data/live/
```

证书应该位于：
```
/etc/letsencrypt/live/freessl.shi021.cn/
├── cert.pem
├── chain.pem
├── fullchain.pem
└── privkey.pem
```

### 服务启动检查

```bash
# 启动所有服务
docker compose -f free_ssl_service/docker-compose.prod.yml up -d

# 检查所有容器运行状态
docker compose ps

# 应该看到 8 个容器状态为 Up
```

### 网络连通性检查

```bash
# 从服务器内部检查
curl http://localhost:80
curl https://localhost:443 -k

# 从外部检查（在本地电脑）
curl https://freessl.shi021.cn
```

## 配置文件最终版本

### nginx.conf 关键配置

```nginx
server {
    listen 80;
    server_name freessl.shi021.cn www.freessl.shi021.cn;
    # ...
}

server {
    listen 443 ssl http2;
    server_name freessl.shi021.cn www.freessl.shi021.cn;

    ssl_certificate /etc/letsencrypt/live/freessl.shi021.cn/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/freessl.shi021.cn/privkey.pem;
    # ...
}
```

### docker-compose.prod.yml 关键配置

```yaml
frontend:
  expose:
    - "8080"  # 与 Dockerfile 一致
  environment:
    - VUE_APP_API_URL=https://freessl.shi021.cn/api  # 正确的域名

nginx:
  ports:
    - "80:80"
    - "443:443"  # 暴露到宿主机
```

## 常见问题

### Q1: 证书域名不匹配

**症状**: Nginx 启动失败，SSL 错误

**解决**:
```bash
# 删除旧证书
docker volume rm freessl_certbot-config

# 重新获取证书
docker compose run --rm certbot certonly --webroot \
    -w /var/www/certbot \
    -d freessl.shi021.cn \
    -d www.freessl.shi021.cn
```

### Q2: 前端无法连接后端

**症状**: 浏览器显示网络错误

**检查**:
1. `VUE_APP_API_URL` 是否正确
2. Nginx 反向代理配置是否正确

### Q3: 80/443 端口被占用

**症状**: Nginx 容器启动失败

**解决**:
```bash
# 查找占用端口的进程
sudo netstat -tlnp | grep -E ':80|:443'

# 停止冲突的服务
sudo systemctl stop apache2
sudo systemctl stop nginx
```

## 下一步

1. 登录远端服务器
2. 按照 `docs/ubuntu-deployment-guide.md` 部署
3. 获取 SSL 证书
4. 启动服务
5. 验证 HTTPS 访问
