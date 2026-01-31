import jwt
from datetime import datetime, timedelta
from flask import current_app, request
from werkzeug.exceptions import Unauthorized
from models.user_model import User

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
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return None
        return user
    
    @staticmethod
    def get_current_user():
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            raise Unauthorized('Missing or invalid authorization header')
        
        user_id = AuthService.decode_token(token[7:])
        user = User.query.get(user_id)
        if not user:
            raise Unauthorized('User not found')
        return user