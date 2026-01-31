# Free SSL 服务

本项目旨在为中小企业和个人网站主提供免费SSL证书服务。

## 功能

1. 用户注册和登录
2. 用户证书管理
3. 证书有效期管理：到期提醒和续期功能
4. 3个月后证书续期需要付费
5. 分享与邀请激励
6. 页面美观。用户操作体验和视觉体验好。

## 技术架构

- 前端: Vue.js + Element UI
- 后端: Python/Flask
- 数据库: MariaDB
- 任务调度: Celery
- 邮件通知: SendGrid/Mailgun

## 安装和运行

### 环境准备

1. **安装Docker**：
   - [Docker安装指南](https://docs.docker.com/get-docker/)
   
2. **克隆代码**：
   ```bash
   git clone https://github.com/yourrepo/free-ssl-service.git
   cd free-ssl-service
   ```

3. **设置环境变量**：
   - 根据`.env.sample`创建`.env`文件，并设置所有必要的环境变量（如MariaDB连接信息、Celery配置、Certbot路径、邮件服务API密钥等）。

### 启动项目

```bash
docker-compose up --build
```

### 访问网站

- 前端应用将在`http://localhost:8080`上运行。
- 后端API将在`http://localhost:5000`上运行。

## 目录结构

```
free_ssl_service/
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── Dockerfile
│   ├── .env.example
│   ├── models/
│   │   ├── user_model.py
│   │   └── cert_model.py
│   ├── routes/
│   │   ├── auth_routes.py
│   │   └── cert_routes.py
│   ├── services/
│   │   ├── auth_service.py
│   │   └── cert_service.py
│   └── requirements.txt
├── frontend/
│   ├── Dockerfile
│   └── src/
│       ├── App.vue
│       ├── main.js
│       ├── components/
│       │   └── Navbar.vue
│       ├── router/
│       │   └── index.js
│       ├── store/
│       │   ├── index.js
│       │   └── modules/
│       │       ├── auth.js
│       │       └── certs.js
│       └── views/
│           ├── Auth/
│           │   ├── Login.vue
│           │   ├── Register.vue
│           │   └── Renew.vue
│           ├── Certificates/
│           │   ├── Create.vue
│           │   ├── Detail.vue
│           │   ├── List.vue
│           │   └── Renew.vue
│           └── Dashboard.vue
├── docker-compose.yml
└── .env.sample
```

## 贡献

如果您希望贡献代码，请提交Pull Request。

## 许可证

本项目采用MIT许可证。
