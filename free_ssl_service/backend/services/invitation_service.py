import secrets
import string
from datetime import datetime, timedelta
from flask import current_app
from models.invitation_model import Invitation, db
from models.user_model import User

class InvitationService:
    @staticmethod
    def generate_invite_code(length=16):
        """
        生成邀请码
        """
        alphabet = string.ascii_uppercase + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    @staticmethod
    def create_invitation(user_id):
        """
        创建邀请码
        """
        invite_code = InvitationService.generate_invite_code()
        
        invitation = Invitation(
            invite_code=invite_code,
            inviter_id=user_id,
            status='pending',
            expires_at=datetime.now() + timedelta(days=30)  # 30天有效期
        )
        db.session.add(invitation)
        db.session.commit()
        
        return invitation
    
    @staticmethod
    def accept_invitation(invite_code, invitee_id):
        """
        接受邀请
        """
        invitation = Invitation.query.filter_by(invite_code=invite_code).first()
        
        if not invitation:
            raise Exception("Invalid invitation code")
        
        if invitation.status != 'pending':
            raise Exception("Invitation already used or expired")
        
        if invitation.expires_at < datetime.now():
            invitation.status = 'expired'
            db.session.commit()
            raise Exception("Invitation expired")
        
        # 更新邀请状态
        invitation.invitee_id = invitee_id
        invitation.status = 'accepted'
        invitation.accepted_at = datetime.now()
        
        # 给邀请者和被邀请者奖励积分
        reward_points = 100  # 奖励100积分
        
        inviter = User.query.get(invitation.inviter_id)
        if inviter:
            inviter.reward_points += reward_points
        
        invitee = User.query.get(invitee_id)
        if invitee:
            invitee.reward_points += reward_points
        
        invitation.reward_points = reward_points
        
        db.session.commit()
        
        return invitation
    
    @staticmethod
    def get_user_invitations(user_id):
        """
        获取用户的邀请列表
        """
        invitations = Invitation.query.filter_by(inviter_id=user_id).order_by(
            Invitation.created_at.desc()
        ).all()
        
        return [inv.to_dict() for inv in invitations]
    
    @staticmethod
    def get_invitation_stats(user_id):
        """
        获取邀请统计
        """
        invitations = Invitation.query.filter_by(inviter_id=user_id).all()
        
        total = len(invitations)
        accepted = len([inv for inv in invitations if inv.status == 'accepted'])
        pending = len([inv for inv in invitations if inv.status == 'pending'])
        expired = len([inv for inv in invitations if inv.status == 'expired'])
        total_rewards = sum([inv.reward_points for inv in invitations])
        
        return {
            'total': total,
            'accepted': accepted,
            'pending': pending,
            'expired': expired,
            'total_rewards': total_rewards
        }