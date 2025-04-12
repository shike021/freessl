import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'default_secret_key'
    
    # MariaDB configuration
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('MARIADB_USER')}:{os.getenv('MARIADB_PASS')}@"
        f"{os.getenv('MARIADB_HOST')}:{os.getenv('MARIADB_PORT')}/{os.getenv('MARIADB_DB')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    
    # Celery configuration
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
    
    # Certbot configuration
    CERTBOT_CONFIG_DIR = os.getenv('CERTBOT_CONFIG_DIR')
    CERTBOT_WORK_DIR = os.getenv('CERTBOT_WORK_DIR')
    CERTBOT_LOG_DIR = os.getenv('CERTBOT_LOG_DIR')
    
    # Email configuration
    EMAIL_SERVICE = os.getenv('EMAIL_SERVICE')
    EMAIL_API_KEY = os.getenv('EMAIL_API_KEY')
