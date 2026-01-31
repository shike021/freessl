# Free SSL 服务

本项目旨在为中小企业和个人网站主提供免费SSL证书服务。

## 功能特性

### 用户管理
- 用户注册和登录
- 邮箱验证
- 密码重置
- JWT认证
- 邀请激励系统

### 证书管理
- SSL证书申请
- 证书列表查看
- 证书详情查看
- 证书续期功能
- 证书到期提醒
- 免费期管理（3个月免费期）

### 支付功能
- 支付宝支付
- 微信支付
- 订单管理
- 支付回调处理

### 安全措施
- CSRF保护
- 请求频率限制（Rate Limiting）
- 敏感数据加密
- HTTPS配置
- Let's Encrypt自动续期

### 任务调度
- Celery任务队列
- 自动检查证书到期
- 自动检查免费期结束
- 自动续期已付费证书
- 邮件通知提醒

### 测试和文档
- 后端单元测试（pytest）
- 前端单元测试（Jest）
- API文档（Swagger/OpenAPI）
- 完整的重构文档

## 技术架构

### 后端
- **框架**: Flask 2.0.1
- **ORM**: Flask-SQLAlchemy 2.5.1
- **数据库**: MariaDB 10.6
- **任务队列**: Celery 5.2.3 + Redis 7
- **邮件服务**: SendGrid
- **SSL证书**: Certbot
- **认证**: JWT (PyJWT 2.1.0)
- **API文档**: Flasgger (Swagger/OpenAPI)
- **安全**: Flask-WTF (CSRF), Flask-Limiter (Rate Limiting), Cryptography (加密)

### 前端
- **框架**: Vue.js 2.6.14
- **UI库**: Element UI 2.15.7
- **状态管理**: Vuex 3.6.2
- **路由**: Vue Router 3.5.3
- **HTTP客户端**: Axios 0.21.1
- **测试**: Jest + @vue/test-utils

### 基础设施
- **容器化**: Docker + Docker Compose
- **反向代理**: Nginx
- **网络**: 自定义bridge网络
- **数据持久化**: Docker volumes

## 安装和运行

### 环境准备

1. **安装Docker和Docker Compose**：
   - [Docker安装指南](https://docs.docker.com/get-docker/)
   - [Docker Compose安装指南](https://docs.docker.com/compose/install/)
   
2. **克隆代码**：
   ```bash
   git clone https://github.com/yourrepo/free-ssl-service.git
   cd free-ssl-service
   ```

3. **设置环境变量**：
   ```bash
   # 复制环境变量模板
   cp free_ssl_service/.env.sample free_ssl_service/.env
   
   # 编辑.env文件，设置必要的环境变量
   vim free_ssl_service/.env
   ```

   **需要配置的关键变量**：
   - `EMAIL_API_KEY`: SendGrid API密钥
   - `EMAIL_FROM`: 发件人邮箱地址
   - `SECRET_KEY`: Flask密钥（生产环境必须修改为随机字符串）
   - `ENCRYPTION_KEY`: 加密密钥（必须是32字节）
   - `MARIADB_PASS`: 数据库密码（生产环境必须修改）

### 启动项目

```bash
# 开发环境
docker-compose -f free_ssl_service/docker-compose.yml up --build

# 生产环境（需要先配置docker-compose.prod.yml）
docker-compose -f free_ssl_service/docker-compose.prod.yml up --build -d
```

### 访问地址

- **前端应用**: http://localhost:8080
- **后端API**: http://localhost:5000
- **API文档**: http://localhost:5000/apidocs
- **MariaDB**: localhost:3306
- **Redis**: localhost:6379

### 获取SSL证书

首次启动后，需要获取Let's Encrypt SSL证书：

```bash
# 进入certbot容器
docker-compose exec certbot sh

# 申请证书（替换为你的域名）
certbot certonly --webroot -w /var/www/certbot -d yourdomain.com -d www.yourdomain.com

# 退出容器
exit

# 重启nginx
docker-compose restart nginx
```

## 测试

### 后端测试

```bash
# 进入后端容器
docker-compose exec backend sh

# 运行所有测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=. --cov-report=html

# 退出容器
exit
```

### 前端测试

```bash
# 进入前端容器
docker-compose exec frontend sh

# 运行所有测试
npm run test:unit

# 退出容器
exit
```

## 开发

### 开发环境配置

1. **后端开发**：
   ```bash
   # 进入后端容器
   docker-compose exec backend sh
   
   # 安装新的依赖
   pip install package-name
   
   # 更新requirements.txt
   pip freeze > requirements.txt
   ```

2. **前端开发**：
   ```bash
   # 进入前端容器
   docker-compose exec frontend sh
   
   # 安装新的依赖
   npm install package-name
   ```

3. **查看日志**：
   ```bash
   # 查看所有服务日志
   docker-compose logs -f
   
   # 查看特定服务日志
   docker-compose logs -f backend
   docker-compose logs -f frontend
   docker-compose logs -f celery-worker
   ```

### 代码规范

**后端（Python）**：
- 使用 `.flake8` 配置文件
- 运行代码检查：`flake8 .`
- 运行代码质量检查：`pylint **/*.py`

**前端（JavaScript/Vue）**：
- 使用 `.eslintrc.js` 配置文件
- 运行代码检查：`npm run lint`

## 部署

### 生产环境部署

1. **配置生产环境变量**：
   ```bash
   cp free_ssl_service/.env.sample free_ssl_service/.env.production
   # 编辑.env.production，设置生产环境变量
   ```

2. **使用生产环境配置启动**：
   ```bash
   docker-compose -f free_ssl_service/docker-compose.prod.yml up -d
   ```

3. **配置域名和SSL证书**：
   - 确保域名已解析到服务器IP
   - 使用Let's Encrypt获取SSL证书
   - 配置Nginx反向代理

4. **配置防火墙**：
   ```bash
   # 开放HTTP和HTTPS端口
   ufw allow 80/tcp
   ufw allow 443/tcp
   ```

### 备份

```bash
# 备份数据库
docker-compose exec mariadb mysqldump -u freessl -pfreessl_password freessl > backup.sql

# 备份证书
docker run --rm -v freessl_certbot-config:/data -v $(pwd):/backup alpine tar czf /backup/certbot-backup.tar.gz -C /data .
```

## 故障排查

### 常见问题

1. **容器无法启动**：
   - 检查端口是否被占用：`netstat -tlnp | grep -E ':(80|443|5000|3306|6379)'`
   - 检查Docker日志：`docker-compose logs`
   - 检查环境变量配置

2. **数据库连接失败**：
   - 确认MariaDB容器已启动：`docker-compose ps`
   - 检查数据库连接配置
   - 查看后端日志：`docker-compose logs backend`

3. **邮件发送失败**：
   - 检查SendGrid API密钥是否正确
   - 检查网络连接
   - 查看Celery日志：`docker-compose logs celery-worker`

4. **SSL证书问题**：
   - 确认域名已正确解析
   - 检查Nginx配置
   - 手动续期证书：`docker-compose exec certbot certbot renew`

### 查看日志

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f celery-worker
docker-compose logs -f celery-beat
docker-compose logs -f nginx

# 查看最近100行日志
docker-compose logs --tail=100
```

## 文档

- [优化历史](docs/optimization-history.md) - 项目完整优化历史
- [API文档](http://localhost:5000/apidocs) - Swagger/OpenAPI文档
- [部署文档](docs/deployment.md) - 详细部署指南
- [开发文档](docs/development.md) - 开发指南
- [故障排查](docs/troubleshooting.md) - 常见问题解决

## 贡献

如果您希望贡献代码，请遵循以下步骤：

1. Fork本仓库
2. 创建特性分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -m 'Add some feature'`
4. 推送到分支：`git push origin feature/your-feature`
5. 提交Pull Request

请确保：
- 代码符合项目规范
- 添加必要的测试
- 更新相关文档
- 提交信息清晰明确

## 许可证

本项目采用MIT许可证。详见 [LICENSE](LICENSE) 文件。

## 更新日志

详细的版本更新记录请查看 [CHANGELOG.md](CHANGELOG.md)。

## 联系方式

- 项目主页: https://github.com/yourrepo/free-ssl-service
- 问题反馈: https://github.com/yourrepo/free-ssl-service/issues

## 致谢

感谢所有为本项目做出贡献的开发者。

## 目录结构

```
freessl/
├── docs/                          # 文档目录
│   ├── optimization-history.md   # 优化历史
│   ├── api.md                    # API文档
│   ├── deployment.md             # 部署文档
│   ├── development.md            # 开发文档
│   └── troubleshooting.md        # 故障排查文档
├── scripts/                      # 脚本目录
│   ├── deploy.sh                # 部署脚本
│   ├── backup.sh                # 备份脚本
│   └── setup.sh                 # 初始化脚本
├── free_ssl_service/            # 主项目目录
│   ├── backend/
│   │   ├── app.py              # Flask应用入口
│   │   ├── config.py           # 配置文件
│   │   ├── Dockerfile          # 后端Docker镜像
│   │   ├── requirements.txt     # Python依赖
│   │   ├── .env.sample         # 环境变量模板
│   │   ├── tasks.py            # Celery任务
│   │   ├── models/             # 数据模型
│   │   │   ├── __init__.py
│   │   │   ├── db.py          # 数据库实例
│   │   │   ├── user_model.py  # 用户模型
│   │   │   ├── cert_model.py  # 证书模型
│   │   │   ├── payment_model.py  # 支付订单模型
│   │   │   └── invitation_model.py  # 邀请模型
│   │   ├── routes/             # 路由
│   │   │   ├── __init__.py
│   │   │   ├── auth_routes.py  # 认证路由
│   │   │   ├── cert_routes.py  # 证书路由
│   │   │   ├── payment_routes.py  # 支付路由
│   │   │   └── invitation_routes.py  # 邀请路由
│   │   ├── services/           # 业务逻辑
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py  # 认证服务
│   │   │   ├── cert_service.py  # 证书服务
│   │   │   ├── email_service.py  # 邮件服务
│   │   │   ├── payment_service.py  # 支付服务
│   │   │   └── invitation_service.py  # 邀请服务
│   │   ├── utils/              # 工具函数
│   │   │   ├── __init__.py
│   │   │   ├── error_handler.py  # 错误处理
│   │   │   └── encryption.py   # 加密工具
│   │   └── tests/              # 测试
│   │       ├── __init__.py
│   │       └── test_api.py     # API测试
│   ├── frontend/
│   │   ├── public/             # 静态资源
│   │   ├── src/
│   │   │   ├── main.js        # 入口文件
│   │   │   ├── App.vue        # 根组件
│   │   │   ├── components/    # 公共组件
│   │   │   │   └── Navbar.vue
│   │   │   ├── views/         # 页面组件
│   │   │   │   ├── Auth/      # 认证页面
│   │   │   │   │   ├── Login.vue
│   │   │   │   │   ├── Register.vue
│   │   │   │   │   ├── ForgotPassword.vue
│   │   │   │   │   └── ResetPassword.vue
│   │   │   │   ├── Certificates/  # 证书页面
│   │   │   │   │   ├── List.vue
│   │   │   │   │   ├── Create.vue
│   │   │   │   │   ├── Detail.vue
│   │   │   │   │   └── Renew.vue
│   │   │   │   └── Dashboard.vue
│   │   │   ├── router/        # 路由配置
│   │   │   │   └── index.js
│   │   │   ├── store/         # 状态管理
│   │   │   │   ├── index.js
│   │   │   │   └── modules/
│   │   │   │       ├── auth.js
│   │   │   │       └── certs.js
│   │   │   └── utils/         # 工具函数
│   │   │       └── api.js     # API配置
│   │   ├── tests/             # 测试
│   │   │   └── unit/
│   │   │       └── auth.spec.js
│   │   ├── package.json       # 前端依赖
│   │   ├── vue.config.js      # Vue配置
│   │   ├── jest.config.js     # Jest配置
│   │   ├── babel.config.js    # Babel配置
│   │   ├── .env.development   # 开发环境变量
│   │   ├── .env.production    # 生产环境变量
│   │   ├── .eslintrc.js       # ESLint配置
│   │   ├── .prettierrc        # Prettier配置
│   │   └── Dockerfile         # 前端Docker镜像
│   ├── nginx/
│   │   └── nginx.conf         # Nginx配置
│   ├── docker-compose.yml     # Docker Compose配置
│   ├── docker-compose.dev.yml  # 开发环境配置
│   ├── docker-compose.prod.yml # 生产环境配置
│   └── .env.sample           # 环境变量模板
├── README.md                   # 项目说明
├── CHANGELOG.md                # 版本更新日志
├── LICENSE                     # MIT许可证
└── .gitignore                  # Git忽略文件
```

## 贡献

如果您希望贡献代码，请提交Pull Request。

## 许可证

本项目采用MIT许可证。

## 开发说明
本项目由AI辅助开发完成。
