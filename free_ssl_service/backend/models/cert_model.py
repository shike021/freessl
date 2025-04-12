from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Certificate(Base):
    __tablename__ = 'certificates'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)  # 关联用户ID
    domains = Column(String(255), nullable=False)
    email = Column(String(120), nullable=False)
    issue_date = Column(DateTime, default=datetime.now)
    expiry_date = Column(DateTime, nullable=False)
    free_expiry_date = Column(DateTime, nullable=False)
    cert_path = Column(String(255), nullable=False)
    notified_free_expiry = Column(Boolean, default=False)
    payment_status = Column(String(20), default='free')
