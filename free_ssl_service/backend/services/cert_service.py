import os
import subprocess
from datetime import datetime, timedelta
from flask import current_app
from models.cert_model import Certificate, db

class CertService:
    def __init__(self):
        pass
    
    def issue_cert(self, domains, email, user):
        """
        使用certbot颁发证书
        """
        cmd = [
            'certbot', 'certonly', '--non-interactive', '--agree-tos',
            '--email', email,
            '--dns-route53',
            '--domains', domains,
            '--config-dir', current_app.config['CERTBOT_CONFIG_DIR'],
            '--work-dir', current_app.config['CERTBOT_WORK_DIR'],
            '--logs-dir', current_app.config['CERTBOT_LOG_DIR']
        ]
        
        try:
            subprocess.run(cmd, check=True)
            cert = self._save_cert_to_db(domains, email, user)
            return cert
        except subprocess.CalledProcessError as e:
            raise Exception(f"Certificate issuance failed: {str(e)}")
    
    def _save_cert_to_db(self, domains, email, user):
        cert_path = f"{current_app.config['CERTBOT_CONFIG_DIR']}/live/{domains.split(',')[0]}"
        expiry_date = self._get_expiry_date(cert_path)
        
        # 免费期为3个月
        free_expiry_date = datetime.now() + timedelta(days=90)
        
        cert = Certificate(
            user_id=user.id,
            domains=domains,
            email=email,
            issue_date=datetime.now(),
            expiry_date=expiry_date,
            free_expiry_date=free_expiry_date,
            cert_path=cert_path,
            payment_status='free'
        )
        db.session.add(cert)
        db.session.commit()
        return cert
    
    def _get_expiry_date(self, cert_path):
        cmd = ['openssl', 'x509', '-enddate', '-noout', '-in', f'{cert_path}/cert.pem']
        result = subprocess.run(cmd, capture_output=True, text=True)
        date_str = result.stdout.split('=')[1].strip()
        return datetime.strptime(date_str, '%b %d %H:%M:%S %Y %Z')
    
    def renew_cert(self, cert_id, user):
        """
        续期证书
        """
        cert = Certificate.query.filter_by(id=cert_id, user_id=user.id).first()
        if not cert:
            raise Exception("Certificate not found")
        
        cmd = [
            'certbot', 'renew', '--non-interactive',
            '--cert-name', cert.domains.split(',')[0],
            '--config-dir', current_app.config['CERTBOT_CONFIG_DIR'],
            '--work-dir', current_app.config['CERTBOT_WORK_DIR'],
            '--logs-dir', current_app.config['CERTBOT_LOG_DIR']
        ]
        
        try:
            subprocess.run(cmd, check=True)
            cert.expiry_date = self._get_expiry_date(cert.cert_path)
            cert.payment_status = 'paid'
            db.session.commit()
            return cert
        except subprocess.CalledProcessError as e:
            raise Exception(f"Certificate renewal failed: {str(e)}")