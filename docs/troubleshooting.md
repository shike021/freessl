# 故障排查文档

## 概述

本文档提供Free SSL Service常见问题的排查和解决方案。

## 容器问题

### 容器无法启动

**症状**: `docker-compose up` 后容器立即退出

**排查步骤**:

1. 查看容器日志
```bash
docker-compose logs <service-name>
docker-compose logs --tail=100
```

2. 检查容器状态
```bash
docker-compose ps
```

3. 检查端口占用
```bash
netstat -tlnp | grep -E ':(80|443|5000|3306|6379)'
```

**常见原因和解决方案**:

- **端口被占用**: 修改 `docker-compose.yml` 中的端口映射
- **环境变量缺失**: 检查 `.env` 文件是否正确配置
- **磁盘空间不足**: 清理Docker缓存和未使用的镜像
```bash
docker system prune -a
```

### 容器频繁重启

**症状**: 容器状态显示 `Restarting`

**排查步骤**:

1. 查看重启次数
```bash
docker-compose ps
```

2. 查看日志
```bash
docker-compose logs -f <service-name>
```

**常见原因**:

- **健康检查失败**: 检查服务是否正常响应
- **内存不足**: 增加服务器内存或优化服务配置
- **配置错误**: 检查配置文件语法

## 数据库问题

### 数据库连接失败

**症状**: 后端日志显示数据库连接错误

**排查步骤**:

1. 检查MariaDB容器状态
```bash
docker-compose ps mariadb
```

2. 检查数据库日志
```bash
docker-compose logs mariadb
```

3. 测试数据库连接
```bash
docker-compose exec backend python -c "
from app import app
with app.app_context():
    from models.db import db
    db.session.execute('SELECT 1')
    print('Database connection OK')
"
```

**解决方案**:

- **环境变量错误**: 检查 `.env` 中的数据库配置
- **容器网络问题**: 确保所有容器在同一网络中
- **数据库未启动**: 重启MariaDB容器
```bash
docker-compose restart mariadb
```

### 数据库性能问题

**症状**: 查询响应缓慢

**排查步骤**:

1. 查看数据库进程
```bash
docker-compose exec mariadb mysqladmin -u freessl -p processlist
```

2. 查看慢查询日志
```bash
docker-compose exec mariadb cat /var/log/mysql/slow.log
```

**解决方案**:

- **添加索引**: 为常用查询字段添加索引
- **优化查询**: 重写复杂的SQL查询
- **增加缓存**: 使用Redis缓存常用数据
- **调整配置**: 增加 `innodb_buffer_pool_size`

## 后端问题

### API请求失败

**症状**: 前端无法调用后端API

**排查步骤**:

1. 检查后端服务状态
```bash
curl -I http://localhost:5000
```

2. 查看后端日志
```bash
docker-compose logs backend
```

3. 检查网络连接
```bash
docker-compose exec frontend ping backend
```

**解决方案**:

- **服务未启动**: 重启后端容器
- **端口配置错误**: 检查 `docker-compose.yml` 中的端口映射
- **防火墙阻止**: 开放5000端口
```bash
sudo ufw allow 5000/tcp
```

### Celery任务不执行

**症状**: 定时任务或异步任务不执行

**排查步骤**:

1. 检查Celery Worker状态
```bash
docker-compose ps celery-worker
```

2. 查看Celery日志
```bash
docker-compose logs celery-worker
```

3. 检查Redis连接
```bash
docker-compose exec backend python -c "
from celery import Celery
celery = Celery('tasks', broker='redis://redis:6379/0')
print('Redis connection OK')
"
```

**解决方案**:

- **Redis未启动**: 启动Redis容器
- **任务未注册**: 检查 `tasks.py` 中的任务定义
- **队列配置错误**: 检查 `CELERY_BROKER_URL` 配置

## 前端问题

### 页面无法访问

**症状**: 浏览器无法打开前端页面

**排查步骤**:

1. 检查前端服务状态
```bash
curl -I http://localhost:8080
```

2. 查看前端日志
```bash
docker-compose logs frontend
```

3. 检查Nginx配置（如果使用）
```bash
sudo nginx -t
```

**解决方案**:

- **构建失败**: 重新构建前端镜像
```bash
docker-compose build frontend
```

- **端口被占用**: 修改端口映射
- **静态文件缺失**: 检查 `dist/` 目录是否存在

### API调用失败

**症状**: 前端调用后端API返回错误

**排查步骤**:

1. 打开浏览器开发者工具，查看Network标签
2. 检查请求URL是否正确
3. 查看响应状态码和错误信息

**解决方案**:

- **CORS问题**: 配置后端允许跨域
- **Token过期**: 重新登录获取新Token
- **API路径错误**: 检查 `src/utils/api.js` 中的配置

## 邮件问题

### 邮件发送失败

**症状**: 用户收不到验证邮件或通知邮件

**排查步骤**:

1. 检查SendGrid API密钥
```bash
echo $EMAIL_API_KEY
```

2. 查看Celery日志
```bash
docker-compose logs celery-worker
```

3. 测试邮件发送
```bash
docker-compose exec backend python -c "
from services.email_service import EmailService
EmailService.send_test_email('your-email@example.com')
"
```

**解决方案**:

- **API密钥无效**: 更新SendGrid API密钥
- **邮件被拒收**: 检查发件人邮箱是否已验证
- **网络问题**: 检查服务器网络连接

## SSL证书问题

### 证书获取失败

**症状**: Certbot无法获取SSL证书

**排查步骤**:

1. 检查域名解析
```bash
nslookup yourdomain.com
dig yourdomain.com
```

2. 检查80端口是否开放
```bash
sudo ufw status
```

3. 查看Certbot日志
```bash
docker-compose logs certbot
```

**解决方案**:

- **域名未解析**: 等待DNS生效或检查DNS配置
- **端口未开放**: 开放80和443端口
- **Nginx配置错误**: 检查Nginx配置文件

### 证书过期

**症状**: 浏览器提示证书过期

**解决方案**:

```bash
# 手动续期证书
docker-compose exec certbot certbot renew

# 重启Nginx
docker-compose restart nginx

# 检查证书有效期
docker-compose exec certbot certbot certificates
```

## 支付问题

### 支付回调失败

**症状**: 支付成功但订单状态未更新

**排查步骤**:

1. 查看支付服务日志
```bash
docker-compose logs backend | grep payment
```

2. 检查支付网关配置
```bash
echo $ALIPAY_APP_ID
echo $WECHAT_MCH_ID
```

3. 测试回调接口
```bash
curl -X POST http://localhost:5000/api/payment/callback/alipay \
  -H "Content-Type: application/json" \
  -d '{"order_id":"test","status":"success"}'
```

**解决方案**:

- **签名验证失败**: 检查公钥和私钥配置
- **回调URL错误**: 检查支付网关配置的回调地址
- **网络问题**: 确保支付网关可以访问你的服务器

## 性能问题

### 响应缓慢

**症状**: 页面加载或API响应慢

**排查步骤**:

1. 查看系统资源使用
```bash
docker stats
free -h
df -h
```

2. 查看服务日志
```bash
docker-compose logs --tail=100
```

3. 使用性能分析工具
```bash
# 后端
docker-compose exec backend python -m cProfile -s time app.py

# 前端
# 使用Chrome DevTools Performance标签
```

**解决方案**:

- **数据库查询慢**: 优化SQL查询，添加索引
- **内存不足**: 增加服务器内存
- **CPU占用高**: 优化代码，使用缓存
- **网络延迟**: 使用CDN加速

## 日志分析

### 查看日志

```bash
# 查看所有服务日志
docker-compose logs

# 查看特定服务日志
docker-compose logs backend
docker-compose logs frontend
docker-compose logs celery-worker

# 实时查看日志
docker-compose logs -f

# 查看最近100行日志
docker-compose logs --tail=100

# 查看特定时间的日志
docker-compose logs --since 2024-01-01T00:00:00
```

### 日志级别

修改日志级别以获取更多或更少的信息：

**后端**:
编辑 `config.py`:
```python
LOG_LEVEL = 'DEBUG'  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

**前端**:
编辑 `vue.config.js`:
```javascript
module.exports = {
  configureWebpack: {
    devtool: 'source-map'
  }
}
```

## 备份和恢复

### 数据库备份

```bash
# 备份数据库
docker-compose exec mariadb mysqldump -u freessl -p$MARIADB_PASS freessl > backup.sql

# 恢复数据库
docker-compose exec -T mariadb mysql -u freessl -p$MARIADB_PASS freessl < backup.sql
```

### 证书备份

```bash
# 备份证书
docker run --rm -v freessl_certbot-config:/data -v $(pwd):/backup alpine tar czf /backup/certbot-backup.tar.gz -C /data .

# 恢复证书
docker run --rm -v freessl_certbot-config:/data -v $(pwd):/backup alpine tar xzf /backup/certbot-backup.tar.gz -C /data
```

## 获取帮助

如果以上方法都无法解决问题：

1. 查看完整日志
```bash
docker-compose logs > logs.txt
```

2. 收集系统信息
```bash
docker version
docker-compose version
docker-compose ps
```

3. 提交Issue
   - 访问 https://github.com/yourrepo/free-ssl-service/issues
   - 提供详细的错误信息和日志
   - 说明操作系统和软件版本

## 相关文档

- [部署文档](deployment.md)
- [开发文档](development.md)
- [API文档](api.md)
