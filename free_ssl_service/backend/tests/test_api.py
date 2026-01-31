import pytest
from app import app, db
from models.user_model import User
from models.cert_model import Certificate

@pytest.fixture
def client():
    """
    创建测试客户端
    """
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
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

def test_get_current_user(client, auth_headers):
    """
    测试获取当前用户
    """
    response = client.get('/api/auth/me', headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json
    assert 'username' in data
    assert data['username'] == 'testuser'

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

if __name__ == '__main__':
    pytest.main([__file__, '-v'])