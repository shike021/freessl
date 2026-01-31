from flask import Blueprint, request, jsonify
from services.auth_service import AuthService
from services.cert_service import CertService
from models.cert_model import Certificate, db
from datetime import datetime, timedelta

cert_bp = Blueprint('cert', __name__, url_prefix='/api/certs')

@cert_bp.route('', methods=['GET'])
def list_certs():
    user = AuthService.get_current_user()
    certs = Certificate.query.filter_by(user_id=user.id).order_by(Certificate.issue_date.desc()).all()
    return jsonify([cert.to_dict() for cert in certs])

@cert_bp.route('', methods=['POST'])
def create_cert():
    user = AuthService.get_current_user()
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
        
        return jsonify(cert.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@cert_bp.route('/<int:cert_id>', methods=['GET'])
def get_cert(cert_id):
    user = AuthService.get_current_user()
    cert = Certificate.query.filter_by(id=cert_id, user_id=user.id).first()
    
    if not cert:
        return jsonify({'error': 'Certificate not found'}), 404
    
    cert_dict = cert.to_dict()
    
    # 读取证书文件
    try:
        cert_dict['certificate'] = open(f"{cert.cert_path}/cert.pem").read()
        cert_dict['private_key'] = open(f"{cert.cert_path}/privkey.pem").read()
        cert_dict['chain'] = open(f"{cert.cert_path}/chain.pem").read()
    except FileNotFoundError:
        return jsonify({'error': 'Certificate files not found'}), 404
    
    return jsonify(cert_dict)

@cert_bp.route('/<int:cert_id>/renew', methods=['POST'])
def renew_cert(cert_id):
    user = AuthService.get_current_user()
    
    try:
        cert_service = CertService()
        cert = cert_service.renew_cert(cert_id, user)
        return jsonify(cert.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400