import os
import subprocess
from datetime import datetime
from models.cert_model import Certificate

class CertService:
    def __init__(self, config):
        self.config = config
    
    def issue_cert(self, domains, email, user):
        """
        使用certbot颁发证书
        """
        cmd = [
            'certbot', 'certonly', '--non-interactive', '--agree-tos',
            '--email', email,
            '--dns-route53',  # 或其他验证方式
            '--domains', domains,
            '--config-dir', self.config.CERTBOT_CONFIG_DIR,
            '--work-dir', self.config.CERTBOT_WORK_DIR,
            '--logs-dir', self.config.CERTBOT_LOG_DIR
        ]
        
        try:
            subprocess.run(cmd, check=True)
            cert = self._save_cert_to_db(domains, email, user)
            return cert
        except subprocess.CalledProcessError as e:
            raise Exception(f"Certificate issuance failed: {str(e)}")
    
    def _save_cert_to_db(self, domains, email, user):
        cert_path = f"{self.config.CERTBOT_CONFIG_DIR}/live/{domains.split(',')[0]}"
        expiry_date = self._get_expiry_date(cert_path)
        
        cert = Certificate(
            user=user,
            domains=domains,
            email=email,
            issue_date=datetime.now(),
            expiry_date=expiry_date,
            cert_path=cert_path
        )
        cert.save()
        return cert
    
    def _get_expiry_date(self, cert_path):
        cmd = ['openssl', 'x509', '-enddate', '-noout', '-in', f'{cert_path}/cert.pem']
        result = subprocess.run(cmd, capture_output=True, text=True)
        date_str = result.stdout.split('=')[1].strip()
        return datetime.strptime(date_str, '%b %d %H:%M:%S %Y %Z')
