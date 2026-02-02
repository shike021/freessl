import jwt
import logging
from datetime import datetime, timedelta
from typing import Optional
from flask import current_app, request
from werkzeug.exceptions import Unauthorized
from models.user_model import User

logger = logging.getLogger(__name__)

class AuthService:
    """
    认证服务类，负责用户认证、令牌生成和验证
    """
    
    @staticmethod
    def generate_token(user_id: int) -> str:
        """
        生成JWT令牌
        
        Args:
            user_id: 用户ID
            
        Returns:
            str: 生成的JWT令牌
        """
        payload = {
            'exp': datetime.now() + timedelta(days=1),  # 令牌有效期1天
            'iat': datetime.now(),  # 令牌签发时间
            'sub': str(user_id)  # 用户ID
        }
        
        try:
            token = jwt.encode(
                payload,
                current_app.config['SECRET_KEY'],
                algorithm='HS256'
            )
            logger.info(f"Generated token for user ID: {user_id}")
            return token
        except Exception as e:
            logger.error(f"Failed to generate token: {str(e)}")
            raise Exception(f"Failed to generate token: {str(e)}")
    
    @staticmethod
    def decode_token(token: str) -> str:
        """
        解码JWT令牌
        
        Args:
            token: JWT令牌
            
        Returns:
            str: 用户ID
            
        Raises:
            Unauthorized: 令牌过期或无效
        """
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            user_id = payload['sub']
            logger.info(f"Decoded token for user ID: {user_id}")
            return user_id
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            raise Unauthorized('Token expired. Please log in again.')
        except jwt.InvalidTokenError:
            logger.warning("Invalid token")
            raise Unauthorized('Invalid token. Please log in again.')
        except Exception as e:
            logger.error(f"Failed to decode token: {str(e)}")
            raise Unauthorized('Invalid token. Please log in again.')
    
    @staticmethod
    def authenticate(username: str, password: str) -> Optional[User]:
        """
        用户认证
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            Optional[User]: 认证成功返回用户对象，失败返回None
        """
        # 参数验证
        if not username or not password:
            logger.warning("Missing username or password")
            return None
        
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            logger.warning(f"Authentication failed for username: {username}")
            return None
        
        logger.info(f"Authentication successful for username: {username}")
        return user
    
    @staticmethod
    def get_current_user() -> User:
        """
        获取当前登录用户
        
        Returns:
            User: 当前用户对象
            
        Raises:
            Unauthorized: 未授权或用户不存在
        """
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            logger.warning("Missing or invalid authorization header")
            raise Unauthorized('Missing or invalid authorization header')
        
        try:
            # 提取令牌（去掉'Bearer '前缀）
            token_value = token[7:]
            user_id = AuthService.decode_token(token_value)
            
            user = User.query.get(user_id)
            if not user:
                logger.warning(f"User not found for ID: {user_id}")
                raise Unauthorized('User not found')
            
            logger.info(f"Retrieved current user: {user.username}")
            return user
        except Unauthorized:
            raise
        except Exception as e:
            logger.error(f"Failed to get current user: {str(e)}")
            raise Unauthorized('Failed to authenticate user')