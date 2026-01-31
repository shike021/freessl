from models.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import re

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(128))
    reset_token = db.Column(db.String(128))
    
    certificates = db.relationship('Certificate', backref='user', lazy=True)

    def set_password(self, password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r'\d', password) or not re.search(r'[A-Za-z]', password):
            raise ValueError("Password must contain both letters and numbers")
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_verification_token(self):
        self.verification_token = generate_password_hash(self.email + str(datetime.now()))[:50]
        return self.verification_token
    
    def generate_reset_token(self):
        self.reset_token = generate_password_hash(self.email + str(datetime.now()))[:50]
        return self.reset_token
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'verified': self.verified
        }