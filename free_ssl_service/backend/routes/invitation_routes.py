from flask import Blueprint, request, jsonify
from services.auth_service import AuthService
from services.invitation_service import InvitationService

invitation_bp = Blueprint('invitation', __name__, url_prefix='/api/invitation')

@invitation_bp.route('/create', methods=['POST'])
def create_invitation():
    """
    创建邀请码
    """
    user = AuthService.get_current_user()
    
    try:
        invitation = InvitationService.create_invitation(user.id)
        return jsonify(invitation.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@invitation_bp.route('/accept', methods=['POST'])
def accept_invitation():
    """
    接受邀请
    """
    user = AuthService.get_current_user()
    data = request.json
    
    invite_code = data.get('invite_code')
    if not invite_code:
        return jsonify({'error': 'Invite code is required'}), 400
    
    try:
        invitation = InvitationService.accept_invitation(invite_code, user.id)
        return jsonify(invitation.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@invitation_bp.route('/list', methods=['GET'])
def list_invitations():
    """
    获取用户的邀请列表
    """
    user = AuthService.get_current_user()
    
    invitations = InvitationService.get_user_invitations(user.id)
    return jsonify(invitations)

@invitation_bp.route('/stats', methods=['GET'])
def get_invitation_stats():
    """
    获取邀请统计
    """
    user = AuthService.get_current_user()
    
    stats = InvitationService.get_invitation_stats(user.id)
    return jsonify(stats)