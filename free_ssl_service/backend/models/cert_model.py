from models.db import db
from datetime import datetime

class Certificate(db.Model):
    __tablename__ = 'certificates'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    domains = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    issue_date = db.Column(db.DateTime, default=datetime.now)
    expiry_date = db.Column(db.DateTime, nullable=False)
    free_expiry_date = db.Column(db.DateTime, nullable=False)
    cert_path = db.Column(db.String(255), nullable=False)
    notified_free_expiry = db.Column(db.Boolean, default=False)
    payment_status = db.Column(db.String(20), default='free')
    
    def to_dict(self):
        return {
            'id': self.id,
            'domains': self.domains,
            'email': self.email,
            'issue_date': self.issue_date.isoformat() if self.issue_date else None,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'free_expiry_date': self.free_expiry_date.isoformat() if self.free_expiry_date else None,
            'cert_path': self.cert_path,
            'notified_free_expiry': self.notified_free_expiry,
            'payment_status': self.payment_status,
            'status': 'active' if self.expiry_date > datetime.now() else 'expired',
            'can_renew': self._can_renew()
        }
    
    def _can_renew(self):
        now = datetime.now()
        return (
            (self.free_expiry_date - now).days <= 30 or
            self.expiry_date <= now
        )