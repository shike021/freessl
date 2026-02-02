import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'dev-secret-key-change-in-production'
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    
    # MariaDB configuration
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('MARIADB_USER', 'root')}:{os.getenv('MARIADB_PASS', 'password')}@"
        f"{os.getenv('MARIADB_HOST', 'mariadb')}:{os.getenv('MARIADB_PORT', '3306')}/{os.getenv('MARIADB_DB', 'freessl')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_ECHO = os.getenv('SQLALCHEMY_ECHO', 'false').lower() == 'true'
    
    # Database connection pool configuration
    SQLALCHEMY_POOL_SIZE = int(os.getenv('SQLALCHEMY_POOL_SIZE', '10'))
    SQLALCHEMY_POOL_TIMEOUT = int(os.getenv('SQLALCHEMY_POOL_TIMEOUT', '30'))
    SQLALCHEMY_POOL_RECYCLE = int(os.getenv('SQLALCHEMY_POOL_RECYCLE', '1800'))
    SQLALCHEMY_MAX_OVERFLOW = int(os.getenv('SQLALCHEMY_MAX_OVERFLOW', '20'))
    
    # Cache configuration
    CACHE_TYPE = os.getenv('CACHE_TYPE', 'redis')
    CACHE_REDIS_URL = os.getenv('CACHE_REDIS_URL', 'redis://redis:6379/1')
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', '3600'))
    CACHE_KEY_PREFIX = os.getenv('CACHE_KEY_PREFIX', 'freessl:')
    
    # Celery configuration
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')
    
    # Certbot configuration
    CERTBOT_CONFIG_DIR = os.getenv('CERTBOT_CONFIG_DIR', '/etc/letsencrypt')
    CERTBOT_WORK_DIR = os.getenv('CERTBOT_WORK_DIR', '/var/lib/letsencrypt')
    CERTBOT_LOG_DIR = os.getenv('CERTBOT_LOG_DIR', '/var/log/letsencrypt')
    
    # Email configuration
    EMAIL_SERVICE = os.getenv('EMAIL_SERVICE', 'sendgrid')
    EMAIL_API_KEY = os.getenv('EMAIL_API_KEY', '')
    EMAIL_FROM = os.getenv('EMAIL_FROM', 'noreply@freessl.com')
    
    # OAuth configuration
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', '')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', '')
    WECHAT_CLIENT_ID = os.getenv('WECHAT_CLIENT_ID', '')
    WECHAT_CLIENT_SECRET = os.getenv('WECHAT_CLIENT_SECRET', '')
    
    # Encryption key for sensitive data
    ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', 'your-encryption-key-32-bytes-long')