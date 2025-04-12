from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
api = Api(app)

# MariaDB configuration
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.getenv('MARIADB_USER')}:{os.getenv('MARIADB_PASS')}@"
    f"{os.getenv('MARIADB_HOST')}:{os.getenv('MARIADB_PORT')}/{os.getenv('MARIADB_DB')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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
