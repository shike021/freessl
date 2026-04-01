# Free SSL 服务

为中小企业和个人网站主提供免费 SSL 证书申请与管理的自动化平台。

**在线演示**: [https://freessl.shi021.cn](https://freessl.shi021.cn)

## 功能特性

### 核心功能
- **SSL 证书管理**: 免费申请、自动续期、到期提醒
- **多域名支持**: 单域名、多域名、通配符证书
- **域名验证**: HTTP 验证 / DNS 验证
- **证书续期**: Let's Encrypt 自动续期（90 天有效期）
- **免费期管理**: 首期为 3 个月免费，付费后可继续续期

### 用户系统
- 用户注册和登录
- 邮箱验证
- 密码重置
- JWT 认证（24 小时有效期）
- 邀请激励系统（奖励积分）

### 支付功能
- 支付宝支付
- 微信支付
- 订单管理
- 支付回调处理

### 安全措施
- CSRF 保护
- 请求频率限制（200 次/天，50 次/小时）
- 敏感数据 Fernet 加密
- HTTPS 配置
- 安全响应头（HSTS, CSP, X-Frame-Options）
- SQL 注入/XSS 防护

### 任务调度
- Celery 任务队列
- 自动检查证书到期（每日 09:00）
- 自动检查免费期结束（每日 09:30）
- 自动续期已付费证书（每日 10:00）
- 邮件通知提醒

## 技术架构

| 层级 | 技术 | 版本 |
|------|------|------|
| **后端** | Flask | 2.0.1 |
| **ORM** | Flask-SQLAlchemy | 2.5.1 |
| **数据库** | MariaDB | 10.6 |
| **任务队列** | Celery + Redis | 5.2.3 + 7 |
| **前端** | Vue.js | 3.3.8 |
| **UI 库** | Element Plus | 2.4.3 |
| **状态管理** | Vuex | 4.1.0 |
| **路由** | Vue Router | 4.2.5 |
| **容器** | Docker Compose | v2 |
| **反向代理** | Nginx | Alpine |

## 快速开始

### 1. 环境准备

```bash
# 安装 Docker 和 Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

### 2. 克隆代码

```bash
git clone https://github.com/freessl-service/free-ssl-service.git
cd free-ssl-service
```

### 3. 配置环境变量

```bash
cp free_ssl_service/.env.sample free_ssl_service/.env
vim free_ssl_service/.env
```

**必须修改的变量**：
```bash
MARIADB_PASS=<强密码>
MYSQL_ROOT_PASSWORD=<强密码>
SECRET_KEY=<随机 32 字节字符串>
ENCRYPTION_KEY=<32 字节加密密钥>
EMAIL_API_KEY=<SendGrid API Key>
```

### 4. 获取 SSL 证书

```bash
docker run --rm -v freessl_certbot-config:/etc/letsencrypt certbot/certbot certonly --webroot \
    -w /var/www/certbot \
    -d yourdomain.com \
    -d www.yourdomain.com
```

### 5. 启动服务

```bash
# 开发环境
docker compose -f free_ssl_service/docker-compose.yml up --build

# 生产环境
docker compose -f free_ssl_service/docker-compose.prod.yml up -d
```

### 6. 访问服务

| 服务 | 地址 |
|------|------|
| 前端 | http://localhost:8080 |
| 后端 API | http://localhost:5000 |
| API 文档 | http://localhost:5000/apidocs |

## 测试

```bash
# 后端测试
docker compose exec backend pytest

# 前端测试
docker compose exec frontend npm run test:unit
```

## 部署

### 生产环境部署

详细部署指南请查看：

- **[Ubuntu 服务器部署指南](docs/ubuntu-deployment-guide.md)** - 完整的 Ubuntu 20.04+ 部署步骤
- **[Docker 配置检查清单](docs/docker-config-checklist.md)** - 部署前检查项

### 快速部署脚本

```bash
# 在 Ubuntu 服务器上运行
cd ~/freessl
bash scripts/deploy.sh
```

## 文档

| 文档 | 描述 |
|------|------|
| [API 文档](http://localhost:5000/apidocs) | Swagger/OpenAPI 接口文档 |
| [开发指南](docs/development.md) | 本地开发和贡献指南 |
| [部署指南](docs/deployment.md) | 详细部署说明 |
| [故障排查](docs/troubleshooting.md) | 常见问题解决 |
| [Ubuntu 部署](docs/ubuntu-deployment-guide.md) | Ubuntu 服务器部署指南 |

## 项目结构

```
freessl/
├── docs/                          # 文档目录
│   ├── api.md                    # API 文档
│   ├── deployment.md             # 部署指南
│   ├── development.md            # 开发指南
│   ├── troubleshooting.md        # 故障排查
│   ├── ubuntu-deployment-guide.md # Ubuntu 部署指南
│   └── docker-config-checklist.md # Docker 配置检查
├── scripts/                       # 运维脚本
│   ├── deploy.sh                 # 部署脚本
│   ├── backup.sh                 # 备份脚本
│   └── setup.sh                  # 初始化脚本
├── free_ssl_service/              # 主项目
│   ├── backend/                  # 后端 (Flask)
│   │   ├── app.py               # 应用入口
│   │   ├── models/              # 数据模型
│   │   ├── routes/              # API 路由
│   │   ├── services/            # 业务逻辑
│   │   └── tests/               # 测试
│   ├── frontend/                 # 前端 (Vue 3)
│   │   ├── src/                 # 源代码
│   │   ├── router/              # 路由配置
│   │   ├── store/               # Vuex 状态
│   │   └── tests/               # 测试
│   └── nginx/                    # Nginx 配置
└── docker-compose*.yml            # Docker Compose 配置
```

## 贡献

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -m 'feat: add your feature'`
4. 推送到分支：`git push origin feature/your-feature`
5. 创建 Pull Request

## 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 更新日志

详见 [CHANGELOG.md](CHANGELOG.md)

## 联系方式

- 项目主页：[GitHub](https://github.com/freessl-service/free-ssl-service)
- 问题反馈：[Issues](https://github.com/freessl-service/free-ssl-service/issues)
