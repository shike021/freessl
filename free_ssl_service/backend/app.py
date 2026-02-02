from flask import Flask, request, abort
from flask_restful import Api
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from flask_cors import CORS
from flasgger import Swagger
from celery import Celery
from dotenv import load_dotenv
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
import re

load_dotenv()

app = Flask(__name__)
app.config.from_object('config.Config')

# Swagger API Documentation
swagger = Swagger(app, template={
    "info": {
        "title": "Free SSL Service API",
        "description": "API documentation for Free SSL Service",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }
    }
})

# CSRF Protection
csrf = CSRFProtect(app)

# Cache initialization
cache = Cache(app)

# Rate Limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri=app.config['CELERY_RESULT_BACKEND']
)

# CORS configuration
CORS(app, resources={
    r"/api/*": {
        "origins": ["*"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Security headers
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'"
    return response

# Input validation middleware
@app.before_request
def validate_request():
    # Validate request size
    if request.content_length and request.content_length > 1024 * 1024 * 10:  # 10MB limit
        abort(413, description="Request entity too large")
    
    # Validate input for common attacks
    if request.method in ['POST', 'PUT', 'PATCH']:
        try:
            if request.is_json:
                data = request.get_json()
                validate_input(data)
        except Exception as e:
            abort(400, description="Invalid request data")

# Input validation function
def validate_input(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (str, bytes)):
                # Check for SQL injection patterns
                sql_patterns = [r'\bor\b', r'\band\b', r'\bunion\b', r'\bselect\b', r'\bfrom\b', r'\bwhere\b', r'\bdrop\b', r'\balter\b']
                for pattern in sql_patterns:
                    if re.search(pattern, str(value), re.IGNORECASE):
                        raise ValueError("Invalid input detected")
                # Check for XSS patterns
                xss_patterns = [r'<script', r'</script>', r'<iframe', r'</iframe>', r'javascript:', r'vbscript:']
                for pattern in xss_patterns:
                    if re.search(pattern, str(value), re.IGNORECASE):
                        raise ValueError("Invalid input detected")
            elif isinstance(value, (dict, list)):
                validate_input(value)
    elif isinstance(data, list):
        for item in data:
            validate_input(item)

# Async support
app.executor = ThreadPoolExecutor(max_workers=10)

# Async helper function
def run_async(func):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(func(*args, **kwargs))
    return wrapper

# Import db from models
from models.db import db
db.init_app(app)

api = Api(app)

# Import models
from models.user_model import User
from models.cert_model import Certificate
from models.payment_model import PaymentOrder
from models.invitation_model import Invitation

# Celery configuration
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    return celery

celery = make_celery(app)

# Import routes
from routes.auth_routes import auth_bp
from routes.cert_routes import cert_bp
from routes.payment_routes import payment_bp
from routes.invitation_routes import invitation_bp

# Import tasks to register them with Celery
import tasks

# Register error handlers
from utils.error_handler import register_error_handlers
register_error_handlers(app)

app.register_blueprint(auth_bp)
app.register_blueprint(cert_bp)
app.register_blueprint(payment_bp)
app.register_blueprint(invitation_bp)

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
