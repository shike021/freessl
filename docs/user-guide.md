# Free SSL Service 用户指南

## 目录

- [简介](#简介)
- [快速开始](#快速开始)
- [用户注册](#用户注册)
- [创建SSL证书](#创建ssl证书)
- [管理证书](#管理证书)
- [证书续期](#证书续期)
- [常见问题](#常见问题)
- [API使用](#api使用)

## 简介

Free SSL Service 是一个免费的SSL证书管理服务，帮助用户轻松获取和管理Let's Encrypt SSL证书。

### 主要功能

- 免费获取Let's Encrypt SSL证书
- 自动续期证书
- 证书状态监控
- 多域名支持
- 通配符证书支持

## 快速开始

### 访问服务

在浏览器中打开服务地址：

```
https://yourdomain.com
```

### 首次使用

1. 注册账户
2. 验证邮箱
3. 添加域名
4. 创建证书

## 用户注册

### 注册流程

1. 点击页面右上角的"注册"按钮
2. 填写注册信息：
   - 用户名
   - 邮箱地址
   - 密码
   - 确认密码
3. 点击"注册"按钮
4. 检查邮箱，点击验证链接完成注册

### 登录

1. 点击页面右上角的"登录"按钮
2. 输入用户名/邮箱和密码
3. 点击"登录"按钮

### 忘记密码

1. 在登录页面点击"忘记密码"
2. 输入注册邮箱
3. 检查邮箱，点击重置密码链接
4. 设置新密码

## 创建SSL证书

### 添加域名

1. 登录后进入"证书管理"页面
2. 点击"添加域名"按钮
3. 输入域名信息：
   - 主域名（如：example.com）
   - 子域名（可选，如：www.example.com）
4. 点击"验证DNS"按钮
5. 按照提示配置DNS记录

### 创建证书

1. 在域名列表中，选择要创建证书的域名
2. 点击"创建证书"按钮
3. 选择证书类型：
   - 单域名证书
   - 多域名证书
   - 通配符证书
4. 填写证书信息：
   - 证书名称
   - 有效期（默认90天）
5. 点击"创建"按钮
6. 等待证书签发（通常1-5分钟）

### 证书验证方式

#### HTTP验证

1. 在服务器上创建验证文件
2. 确保文件可通过HTTP访问
3. 系统自动验证

#### DNS验证

1. 在DNS管理面板添加TXT记录
2. 等待DNS传播（通常10-30分钟）
3. 系统自动验证

## 管理证书

### 查看证书列表

1. 登录后进入"证书管理"页面
2. 查看所有证书及其状态：
   - 已签发
   - 待验证
   - 已过期
   - 续期中

### 证书详情

点击证书名称查看详细信息：

- 证书域名
- 签发时间
- 过期时间
- 证书状态
- 证书内容
- 私钥内容

### 下载证书

1. 进入证书详情页面
2. 点击"下载证书"按钮
3. 选择下载格式：
   - PEM格式
   - PKCS12格式（包含私钥）

### 删除证书

1. 在证书列表中找到要删除的证书
2. 点击"删除"按钮
3. 确认删除操作

**注意**：删除证书后无法恢复，请谨慎操作。

## 证书续期

### 自动续期

系统会在证书过期前30天自动尝试续期。

### 手动续期

1. 在证书列表中找到要续期的证书
2. 点击"续期"按钮
3. 确认续期操作
4. 等待续期完成

### 续期失败处理

如果自动续期失败：

1. 检查DNS配置是否正确
2. 检查服务器是否正常运行
3. 检查验证文件是否可访问
4. 手动触发续期
5. 联系技术支持

## 常见问题

### 证书签发失败

**问题**：证书创建后一直处于"待验证"状态

**解决方案**：
1. 检查DNS记录是否正确配置
2. 等待DNS传播完成（最多48小时）
3. 检查服务器防火墙设置
4. 确认验证文件可访问

### 证书无法使用

**问题**：证书已签发但无法在服务器上使用

**解决方案**：
1. 确认下载了完整的证书链
2. 检查证书格式是否正确
3. 确认私钥与证书匹配
4. 检查服务器配置

### 续期失败

**问题**：证书自动续期失败

**解决方案**：
1. 检查DNS配置是否变更
2. 确认服务器正常运行
3. 手动触发续期
4. 检查系统日志

### 域名验证失败

**问题**：DNS验证一直失败

**解决方案**：
1. 使用DNS查询工具检查TXT记录
2. 确认DNS记录已生效
3. 检查DNS服务商限制
4. 尝试使用HTTP验证方式

## API使用

### 认证

所有API请求都需要在Header中包含认证token：

```
Authorization: Bearer <your_token>
```

### 获取Token

**请求**：

```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

**响应**：

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "your_username",
    "email": "your_email@example.com"
  }
}
```

### 创建证书

**请求**：

```http
POST /api/certificates
Content-Type: application/json
Authorization: Bearer <your_token>

{
  "name": "example.com",
  "domains": ["example.com", "www.example.com"],
  "type": "multi",
  "validation_method": "dns"
}
```

**响应**：

```json
{
  "id": 1,
  "name": "example.com",
  "domains": ["example.com", "www.example.com"],
  "status": "pending",
  "created_at": "2024-01-01T00:00:00Z",
  "expires_at": "2024-04-01T00:00:00Z"
}
```

### 查询证书

**请求**：

```http
GET /api/certificates
Authorization: Bearer <your_token>
```

**响应**：

```json
{
  "certificates": [
    {
      "id": 1,
      "name": "example.com",
      "domains": ["example.com", "www.example.com"],
      "status": "active",
      "created_at": "2024-01-01T00:00:00Z",
      "expires_at": "2024-04-01T00:00:00Z"
    }
  ],
  "total": 1
}
```

### 下载证书

**请求**：

```http
GET /api/certificates/1/download
Authorization: Bearer <your_token>
```

**响应**：

返回PEM格式的证书文件

### 续期证书

**请求**：

```http
POST /api/certificates/1/renew
Authorization: Bearer <your_token>
```

**响应**：

```json
{
  "id": 1,
  "status": "renewing",
  "message": "Certificate renewal initiated"
}
```

### 删除证书

**请求**：

```http
DELETE /api/certificates/1
Authorization: Bearer <your_token>
```

**响应**：

```json
{
  "message": "Certificate deleted successfully"
}
```

### 错误响应

所有错误响应都遵循以下格式：

```json
{
  "error": "error_code",
  "message": "Human readable error message",
  "details": {}
}
```

常见错误码：

- `INVALID_TOKEN`: 认证token无效
- `EXPIRED_TOKEN`: 认证token已过期
- `UNAUTHORIZED`: 未授权访问
- `VALIDATION_ERROR`: 请求参数验证失败
- `CERTIFICATE_NOT_FOUND`: 证书不存在
- `DOMAIN_VALIDATION_FAILED`: 域名验证失败
- `RATE_LIMIT_EXCEEDED`: 请求频率超限

## 最佳实践

### 证书管理

1. **定期检查证书状态**：建议每周检查一次证书状态
2. **提前续期**：不要等到证书过期才续期
3. **备份证书**：下载并备份证书和私钥
4. **监控到期时间**：设置证书到期提醒

### 安全建议

1. **保护私钥**：私钥不应泄露给任何人
2. **使用强密码**：账户密码应包含大小写字母、数字和特殊字符
3. **启用两步验证**：如果可用，启用两步验证
4. **定期更换密码**：建议每3个月更换一次密码

### 性能优化

1. **使用CDN**：将证书部署到CDN加速访问
2. **启用HSTS**：强制使用HTTPS连接
3. **配置OCSP Stapling**：减少SSL握手时间
4. **选择合适的证书类型**：根据需求选择单域名或多域名证书

## 技术支持

如果您遇到任何问题，请通过以下方式联系技术支持：

- 邮箱：support@freessl.com
- 在线客服：访问服务官网
- 文档：查看[完整文档](https://docs.freessl.com)

## 更新日志

### v1.0.0 (2024-01-01)

- 初始版本发布
- 支持Let's Encrypt证书申请
- 支持HTTP和DNS验证
- 支持自动续期
- 提供RESTful API

### v1.1.0 (2024-02-01)

- 新增通配符证书支持
- 优化证书签发速度
- 改进用户界面
- 增加证书批量管理功能
- 修复已知问题

## 许可证

本服务遵循Let's Encrypt服务条款，证书免费提供给所有用户使用。

## 隐私政策

我们重视用户隐私，不会收集或存储用户的敏感信息。详细信息请参阅[隐私政策](https://freessl.com/privacy)。
