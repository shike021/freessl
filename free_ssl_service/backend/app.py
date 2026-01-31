from flask import Flask
from flask_restful import Api
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config.from_object('config.Config')

# CSRF Protection
csrf = CSRFProtect(app)

# Rate Limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri=app.config['CELERY_RESULT_BACKEND']
)

# Import db from models
from models.db import db
db.init_app(app)

api = Api(app)

# Import models
from models.user_model import User
from models.cert_model import Certificate

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

# Import tasks to register them with Celery
import tasks

# Register error handlers
from utils.error_handler import register_error_handlers
register_error_handlers(app)

app.register_blueprint(auth_bp)
app.register_blueprint(cert_bp)

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
