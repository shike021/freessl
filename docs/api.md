# API 文档

## 概述

Free SSL Service 提供RESTful API接口，用于用户认证、证书管理、支付和邀请等功能。

## API 基础信息

- **Base URL**: `https://yourdomain.com/api` (生产环境) 或 `http://localhost:5000/api` (开发环境)
- **认证方式**: JWT Bearer Token
- **响应格式**: JSON
- **字符编码**: UTF-8

## 在线文档

项目集成了Swagger/OpenAPI文档，可以通过以下地址访问：

- **开发环境**: http://localhost:5000/apidocs
- **生产环境**: https://yourdomain.com/apidocs

## 认证

大多数API端点需要JWT认证。在请求头中添加：

```
Authorization: Bearer <your-jwt-token>
```

### 获取Token

通过登录接口获取JWT Token：

```bash
POST /api/auth/login
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

响应：

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "1",
    "username": "your_username",
    "email": "your_email@example.com"
  }
}
```

## API 端点

### 认证相关 (Authentication)

#### 用户注册
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

#### 用户登录
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "string",
  "password": "string"
}
```

#### 获取当前用户信息
```http
GET /api/auth/me
Authorization: Bearer <token>
```

#### 邮箱验证
```http
GET /api/auth/verify/<token>
```

#### 忘记密码
```http
POST /api/auth/forgot-password
Content-Type: application/json

{
  "email": "string"
}
```

#### 重置密码
```http
POST /api/auth/reset-password
Content-Type: application/json

{
  "token": "string",
  "new_password": "string"
}
```

### 证书相关 (Certificates)

#### 获取证书列表
```http
GET /api/certs
Authorization: Bearer <token>
```

#### 获取证书详情
```http
GET /api/certs/<id>
Authorization: Bearer <token>
```

#### 创建证书
```http
POST /api/certs
Authorization: Bearer <token>
Content-Type: application/json

{
  "domain": "string",
  "email": "string"
}
```

#### 续期证书
```http
POST /api/certs/<id>/renew
Authorization: Bearer <token>
```

#### 删除证书
```http
DELETE /api/certs/<id>
Authorization: Bearer <token>
```

### 支付相关 (Payment)

#### 创建订单
```http
POST /api/payment/create-order
Authorization: Bearer <token>
Content-Type: application/json

{
  "cert_id": "string",
  "payment_method": "alipay|wechat"
}
```

#### 支付宝支付
```http
POST /api/payment/alipay
Authorization: Bearer <token>
Content-Type: application/json

{
  "order_id": "string"
}
```

#### 微信支付
```http
POST /api/payment/wechat
Authorization: Bearer <token>
Content-Type: application/json

{
  "order_id": "string"
}
```

#### 支付回调
```http
POST /api/payment/callback/<payment_method>
Content-Type: application/json

{
  "order_id": "string",
  "status": "string",
  "signature": "string"
}
```

#### 获取订单状态
```http
GET /api/payment/order/<order_id>
Authorization: Bearer <token>
```

### 邀请相关 (Invitation)

#### 生成邀请码
```http
POST /api/invitation/generate
Authorization: Bearer <token>
```

#### 接受邀请
```http
POST /api/invitation/accept
Content-Type: application/json

{
  "code": "string"
}
```

#### 获取邀请统计
```http
GET /api/invitation/stats
Authorization: Bearer <token>
```

## 响应状态码

- `200 OK` - 请求成功
- `201 Created` - 资源创建成功
- `400 Bad Request` - 请求参数错误
- `401 Unauthorized` - 未授权或token无效
- `403 Forbidden` - 无权限访问
- `404 Not Found` - 资源不存在
- `429 Too Many Requests` - 请求频率超限
- `500 Internal Server Error` - 服务器内部错误

## 错误响应格式

```json
{
  "error": "错误描述信息"
}
```

## 请求频率限制

- 默认限制：200次/天，50次/小时
- 超过限制会返回 `429 Too Many Requests` 状态码
- 响应头会包含剩余请求次数：

```
X-RateLimit-Limit: 50
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1609459200
```

## 安全说明

1. 所有API请求（除了注册、登录、忘记密码）都需要JWT认证
2. Token有效期为24小时，过期后需要重新登录
3. 敏感数据（如密码）必须通过HTTPS传输
4. 所有POST/PUT/DELETE请求都受CSRF保护

## 测试

使用curl测试API：

```bash
# 登录获取token
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123"}'

# 使用token访问受保护的端点
curl -X GET http://localhost:5000/api/certs \
  -H "Authorization: Bearer <your-token>"
```

使用Postman测试：
1. 导入API文档到Postman
2. 设置环境变量（Base URL, Token等）
3. 运行测试集合

## 版本控制

当前API版本：v1.0.0

API版本通过URL路径控制：`/api/v1/...`

## 变更日志

详细的API变更记录请查看 [CHANGELOG.md](../CHANGELOG.md)。

## 支持

如有问题，请提交 [Issue](https://github.com/yourrepo/free-ssl-service/issues)。
