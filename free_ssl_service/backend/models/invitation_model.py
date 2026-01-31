from models.db import db
from datetime import datetime

class Invitation(db.Model):
    __tablename__ = 'invitations'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    invite_code = db.Column(db.String(32), unique=True, nullable=False)
    inviter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    invitee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, expired
    reward_points = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    accepted_at = db.Column(db.DateTime)
    expires_at = db.Column(db.DateTime)
    
    inviter = db.relationship('User', foreign_keys=[inviter_id], backref='sent_invitations')
    invitee = db.relationship('User', foreign_keys=[invitee_id], backref='received_invitations')
    
    def to_dict(self):
        return {
            'id': self.id,
            'invite_code': self.invite_code,
            'inviter_id': self.inviter_id,
            'invitee_id': self.invitee_id,
            'status': self.status,
            'reward_points': self.reward_points,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'accepted_at': self.accepted_at.isoformat() if self.accepted_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None
        }