from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
import re

Base = declarative_base()

from werkzeug.security import generate_password_hash, check_password_hash
import re
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    verified = Column(Boolean, default=False)
    verification_token = Column(String(128))
    reset_token = Column(String(128))

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
