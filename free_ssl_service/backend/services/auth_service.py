import jwt
from datetime import datetime, timedelta
from flask import current_app, redirect
from werkzeug.exceptions import Unauthorized
from authlib.integrations.flask_client import OAuth
from models.user_model import User

oauth = OAuth(current_app)

# Register Google OAuth
google = oauth.register(
    'google',
    client_id='your_google_client_id',
    client_secret='your_google_client_secret',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid profile email'}
)

# Register WeChat OAuth
wechat = oauth.register(
    'wechat',
    client_id='your_wechat_client_id',
    client_secret='your_wechat_client_secret',
    access_token_url='https://api.weixin.qq.com/sns/oauth2/access_token',
    authorize_url='https://open.weixin.qq.com/connect/qrconnect',
    api_base_url='https://api.weixin.qq.com/sns/',
    client_kwargs={'scope': 'snsapi_login'}
)
class AuthService:
    @staticmethod
    def generate_token(user_id):
        payload = {
            'exp': datetime.now() + timedelta(days=1),
            'iat': datetime.now(),
            'sub': str(user_id)
        }
        return jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
    
    @staticmethod
    def decode_token(token):
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise Unauthorized('Token expired. Please log in again.')
        except jwt.InvalidTokenError:
            raise Unauthorized('Invalid token. Please log in again.')
    
    @staticmethod
    def authenticate(username, password):
        user = User.objects(username=username).first()
        if not user or not user.check_password(password):
            return None
        return user
    
    @staticmethod
    def get_current_user(request):
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            raise Unauthorized('Missing or invalid authorization header')
        
        user_id = AuthService.decode_token(token[7:])
        return User.objects.get(id=user_id)
