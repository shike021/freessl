import pytest
from app import app, db
from models.user_model import User
from models.cert_model import Certificate
from services.auth_service import AuthService
from services.cert_service import CertService

@pytest.fixture
def client():
    """
    创建测试客户端
    """
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

@pytest.fixture
def auth_headers(client):
    """
    创建认证头
    """
    # 注册用户
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'Test1234'
    })
    
    # 登录获取token
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'Test1234'
    })
    
    token = response.json['token']
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def test_user():
    """
    创建测试用户
    """
    user = User(username='testuser', email='test@example.com')
    user.set_password('Test1234')
    return user

# 认证服务测试
def test_auth_service_generate_token():
    """
    测试认证服务生成令牌
    """
    with app.app_context():
        token = AuthService.generate_token(1)
        assert isinstance(token, str)
        assert len(token) > 0

def test_auth_service_decode_token():
    """
    测试认证服务解码令牌
    """
    with app.app_context():
        # 生成令牌
        token = AuthService.generate_token(1)
        # 解码令牌
        user_id = AuthService.decode_token(token)
        assert user_id == '1'

def test_auth_service_authenticate_success(client):
    """
    测试认证服务认证成功
    """
    with app.app_context():
        # 注册用户
        client.post('/api/auth/register', json={
            'username': 'authuser',
            'email': 'auth@example.com',
            'password': 'Test1234'
        })
        
        # 认证用户
        user = AuthService.authenticate('authuser', 'Test1234')
        assert user is not None
        assert user.username == 'authuser'

def test_auth_service_authenticate_failure(client):
    """
    测试认证服务认证失败
    """
    with app.app_context():
        # 注册用户
        client.post('/api/auth/register', json={
            'username': 'authuser',
            'email': 'auth@example.com',
            'password': 'Test1234'
        })
        
        # 认证失败 - 密码错误
        user = AuthService.authenticate('authuser', 'WrongPassword')
        assert user is None
        
        # 认证失败 - 用户不存在
        user = AuthService.authenticate('nonexistent', 'Test1234')
        assert user is None

# API测试
def test_register_user(client):
    """
    测试用户注册
    """
    response = client.post('/api/auth/register', json={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'Test1234'
    })
    
    assert response.status_code == 201
    data = response.json
    assert 'message' in data

def test_register_user_invalid_data(client):
    """
    测试用户注册 - 无效数据
    """
    # 缺少用户名
    response = client.post('/api/auth/register', json={
        'email': 'new@example.com',
        'password': 'Test1234'
    })
    assert response.status_code == 400
    
    # 缺少密码
    response = client.post('/api/auth/register', json={
        'username': 'newuser',
        'email': 'new@example.com'
    })
    assert response.status_code == 400

def test_login_user(client):
    """
    测试用户登录
    """
    # 先注册
    client.post('/api/auth/register', json={
        'username': 'loginuser',
        'email': 'login@example.com',
        'password': 'Test1234'
    })
    
    # 登录
    response = client.post('/api/auth/login', json={
        'username': 'loginuser',
        'password': 'Test1234'
    })
    
    assert response.status_code == 200
    data = response.json
    assert 'token' in data
    assert 'user' in data

def test_login_user_invalid_credentials(client):
    """
    测试用户登录 - 无效凭证
    """
    # 先注册
    client.post('/api/auth/register', json={
        'username': 'loginuser',
        'email': 'login@example.com',
        'password': 'Test1234'
    })
    
    # 登录失败 - 密码错误
    response = client.post('/api/auth/login', json={
        'username': 'loginuser',
        'password': 'WrongPassword'
    })
    assert response.status_code == 401
    
    # 登录失败 - 用户不存在
    response = client.post('/api/auth/login', json={
        'username': 'nonexistent',
        'password': 'Test1234'
    })
    assert response.status_code == 401

def test_get_current_user(client, auth_headers):
    """
    测试获取当前用户
    """
    response = client.get('/api/auth/me', headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json
    assert 'username' in data
    assert data['username'] == 'testuser'

def test_get_current_user_invalid_token(client):
    """
    测试获取当前用户 - 无效令牌
    """
    # 使用无效令牌
    invalid_headers = {'Authorization': 'Bearer invalidtoken'}
    response = client.get('/api/auth/me', headers=invalid_headers)
    
    assert response.status_code == 401

def test_create_certificate(client, auth_headers):
    """
    测试创建证书
    """
    response = client.post('/api/certs', 
        json={'domains': 'example.com'},
        headers=auth_headers
    )
    
    # 注意：实际测试时需要mock certbot命令
    # 这里只测试API端点是否正确
    assert response.status_code in [201, 400]  # 400可能是因为certbot未安装

def test_create_certificate_invalid_data(client, auth_headers):
    """
    测试创建证书 - 无效数据
    """
    # 缺少域名
    response = client.post('/api/certs', 
        json={},
        headers=auth_headers
    )
    assert response.status_code == 400

def test_list_certificates(client, auth_headers):
    """
    测试获取证书列表
    """
    response = client.get('/api/certs', headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json
    assert isinstance(data, list)

def test_unauthorized_access(client):
    """
    测试未授权访问
    """
    response = client.get('/api/certs')
    
    assert response.status_code == 401

# 证书服务测试
def test_cert_service_get_user_certs(test_user):
    """
    测试证书服务获取用户证书
    """
    with app.app_context():
        # 添加用户到数据库
        db.session.add(test_user)
        db.session.commit()
        
        # 创建证书服务实例
        cert_service = CertService()
        # 获取用户证书
        certs = cert_service.get_user_certs(test_user.id)
        assert isinstance(certs, list)

def test_cert_service_get_cert_by_id(test_user):
    """
    测试证书服务根据ID获取证书
    """
    with app.app_context():
        # 添加用户到数据库
        db.session.add(test_user)
        db.session.commit()
        
        # 创建证书服务实例
        cert_service = CertService()
        # 获取不存在的证书
        cert = cert_service.get_cert_by_id(999, test_user.id)
        assert cert is None

if __name__ == '__main__':
    pytest.main([__file__, '-v'])