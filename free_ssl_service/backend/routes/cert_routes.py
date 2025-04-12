from flask import Blueprint, request, jsonify
from services.auth_service import AuthService
from services.cert_service import CertService
from models.cert_model import Certificate
from datetime import datetime, timedelta

cert_bp = Blueprint('cert', __name__, url_prefix='/api/certs')

@cert_bp.route('', methods=['GET'])
def list_certs():
    user = AuthService.get_current_user(request)
    certs = Certificate.objects(user=user).order_by('-issue_date')
    return jsonify([{
        'id': str(cert.id),
        'domains': cert.domains,
        'issue_date': cert.issue_date.isoformat(),
        'expiry_date': cert.expiry_date.isoformat(),
        'free_expiry_date': cert.free_expiry_date.isoformat(),
        'status': 'active' if cert.expiry_date > datetime.now() else 'expired'
    } for cert in certs])

@cert_bp.route('', methods=['POST'])
def create_cert():
    user = AuthService.get_current_user(request)
    data = request.json
    
    if not data.get('domains'):
        return jsonify({'error': 'Domains are required'}), 400
    
    try:
        cert_service = CertService()
        cert = cert_service.issue_cert(
            domains=data['domains'],
            email=user.email,
            user=user
        )
        
        return jsonify({
            'id': str(cert.id),
            'domains': cert.domains,
            'expiry_date': cert.expiry_date.isoformat()
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@cert_bp.route('/<cert_id>', methods=['GET'])
def get_cert(cert_id):
    user = AuthService.get_current_user(request)
    cert = Certificate.objects.get_or_404(id=cert_id, user=user)
    
    # 检查证书是否可续期 (在免费期最后30天内或已过期)
    can_renew = (
        (cert.free_expiry_date - datetime.now()).days <= 30 or
        cert.expiry_date <= datetime.now()
    )
    
    return jsonify({
        'id': str(cert.id),
        'domains': cert.domains,
        'issue_date': cert.issue_date.isoformat(),
        'expiry_date': cert.expiry_date.isoformat(),
        'free_expiry_date': cert.free_expiry_date.isoformat(),
        'status': 'active' if cert.expiry_date > datetime.now() else 'expired',
        'can_renew': can_renew,
        'certificate': open(f"{cert.cert_path}/cert.pem").read(),
        'private_key': open(f"{cert.cert_path}/privkey.pem").read(),
        'chain': open(f"{cert.cert_path}/chain.pem").read()
    })
