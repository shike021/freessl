from models.db import db
from datetime import datetime

class PaymentOrder(db.Model):
    __tablename__ = 'payment_orders'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.String(64), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cert_id = db.Column(db.Integer, db.ForeignKey('certificates.id'), nullable=False)
    amount = db.Column(db.Decimal(10, 2), nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)  # alipay, wechat
    status = db.Column(db.String(20), default='pending')  # pending, paid, failed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.now)
    paid_at = db.Column(db.DateTime)
    transaction_id = db.Column(db.String(128))
    
    user = db.relationship('User', backref='payment_orders')
    certificate = db.relationship('Certificate', backref='payment_orders')
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'user_id': self.user_id,
            'cert_id': self.cert_id,
            'amount': float(self.amount),
            'payment_method': self.payment_method,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'paid_at': self.paid_at.isoformat() if self.paid_at else None,
            'transaction_id': self.transaction_id
        }