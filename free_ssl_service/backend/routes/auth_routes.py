from flask import Blueprint, request, jsonify, url_for
from services.auth_service import AuthService, google, wechat
from models.user_model import User, db
from models.user_model import User
from services.auth_service import AuthService
from services.email_service import EmailService

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        user = User(
            username=data['username'],
            email=data['email']
        )
        user.set_password(data['password'])
        user.generate_verification_token()
        user.save()
        
        # 发送验证邮件
        EmailService.send_verification_email(user)
        
        return jsonify({
            'message': 'User created successfully. Please check your email to verify your account.'
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@auth_bp.route('/login/<provider>')
def oauth_login(provider):
    if provider == 'google':
        redirect_uri = url_for('auth.oauth_authorize', provider='google', _external=True)
        return google.authorize_redirect(redirect_uri)
    
    elif provider == 'wechat':
        redirect_uri = url_for('auth.oauth_authorize', provider='wechat', _external=True)
        return wechat.authorize_redirect(redirect_uri)

@auth_bp.route('/authorize/<provider>')
def oauth_authorize(provider):
    token = None
    
    if provider == 'google':
        token = google.authorize_access_token()
        user_info = google.parse_id_token(token)
        email = user_info.get('email')
        username = user_info.get('name')
        
    elif provider == 'wechat':
        token = wechat.authorize_access_token()
        user_info = wechat.get('userinfo').json()
        email = user_info.get('email')
        username = user_info.get('nickname')
    
    # 检查用户是否已存在
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(
            username=username,
            email=email
        )
        user.set_password('default_oauth_password')  # 设置默认密码
        db.session.add(user)
        db.session.commit()
    
    jwt_token = AuthService.generate_token(user.id)
    return jsonify({'token': jwt_token, 'user': {'id': str(user.id), 'username': user.username, 'email': user.email}})

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    
    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing username or password'}), 400
    
    user = AuthService.authenticate(data['username'], data['password'])
    if not user:
        return jsonify({'error': 'Invalid username or password'}), 401
    
    if not user.verified:
        return jsonify({'error': 'Account not verified. Please check your email.'}), 403
    
    token = AuthService.generate_token(user.id)
    return jsonify({
        'token': token,
        'user': {
            'id': str(user.id),
            'username': user.username,
            'email': user.email
        }
    })

@auth_bp.route('/verify/<token>', methods=['GET'])
def verify(token):
    user = User.objects(verification_token=token).first()
    if not user:
        return jsonify({'error': 'Invalid verification token'}), 400
    
    user.verified = True
    user.verification_token = None
    user.save()
    
    return jsonify({'message': 'Account verified successfully'})

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    email = request.json.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    user = User.objects(email=email).first()
    if user:
        reset_token = user.generate_reset_token()
        user.save()
        EmailService.send_password_reset_email(user, reset_token)
    
    # 即使没有找到用户也返回成功以防止枚举攻击
    return jsonify({'message': 'If the email exists, a reset link has been sent'})

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    token = request.json.get('token')
    new_password = request.json.get('new_password')
    
    if not token or not new_password:
        return jsonify({'error': 'Token and new password are required'}), 400
    
    user = User.objects(reset_token=token).first()
    if not user:
        return jsonify({'error': 'Invalid reset token'}), 400
    
    try:
        user.set_password(new_password)
        user.reset_token = None
        user.save()
        return jsonify({'message': 'Password reset successfully'})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
