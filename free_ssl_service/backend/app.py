from flask import Flask
from flask_restful import Api
from mongoengine import connect
from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
api = Api(app)

# MongoDB configuration
connect(
    db=os.getenv('MONGO_DB'),
    host=os.getenv('MONGO_HOST'),
    port=int(os.getenv('MONGO_PORT')),
    username=os.getenv('MONGO_USER'),
    password=os.getenv('MONGO_PASS')
)

# Celery configuration
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=os.getenv('CELERY_RESULT_BACKEND'),
        broker=os.getenv('CELERY_BROKER_URL')
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

app.register_blueprint(auth_bp)
app.register_blueprint(cert_bp)

if __name__ == '__main__':
    app.run(debug=True)
