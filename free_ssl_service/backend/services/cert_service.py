import os
import subprocess
import logging
from datetime import datetime, timedelta
from typing import Optional, List
from flask import current_app
from models.cert_model import Certificate, db

logger = logging.getLogger(__name__)

class CertService:
    """
    证书服务类，负责SSL证书的申请、续期和管理
    """
    
    def __init__(self):
        """初始化证书服务"""
        pass
    
    def issue_cert(self, domains: str, email: str, user) -> Certificate:
        """
        使用certbot颁发证书
        
        Args:
            domains: 域名列表，以逗号分隔
            email: 联系人邮箱
            user: 当前用户对象
            
        Returns:
            Certificate: 生成的证书对象
            
        Raises:
            ValueError: 参数验证失败
            Exception: 证书颁发失败
        """
        # 参数验证
        if not domains or not email:
            raise ValueError("Domains and email are required")
        
        if not user:
            raise ValueError("User is required")
        
        # 验证域名格式
        domain_list = domains.split(',')
        for domain in domain_list:
            if not domain.strip():
                raise ValueError("Invalid domain format")
        
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
            logger.info(f"Issuing certificate for domains: {domains}")
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            cert = self._save_cert_to_db(domains, email, user)
            logger.info(f"Certificate issued successfully for domains: {domains}")
            return cert
        except subprocess.CalledProcessError as e:
            logger.error(f"Certificate issuance failed: {str(e.stderr)}")
            raise Exception(f"Certificate issuance failed: {str(e)}")
    
    def _save_cert_to_db(self, domains: str, email: str, user) -> Certificate:
        """
        将证书信息保存到数据库
        
        Args:
            domains: 域名列表，以逗号分隔
            email: 联系人邮箱
            user: 当前用户对象
            
        Returns:
            Certificate: 保存的证书对象
        """
        # 获取主域名作为证书路径
        main_domain = domains.split(',')[0].strip()
        cert_path = f"{current_app.config['CERTBOT_CONFIG_DIR']}/live/{main_domain}"
        
        # 获取证书过期日期
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
        
        try:
            db.session.add(cert)
            db.session.commit()
            return cert
        except Exception as e:
            logger.error(f"Failed to save certificate to database: {str(e)}")
            db.session.rollback()
            raise Exception(f"Failed to save certificate: {str(e)}")
    
    def _get_expiry_date(self, cert_path: str) -> datetime:
        """
        获取证书的过期日期
        
        Args:
            cert_path: 证书存放路径
            
        Returns:
            datetime: 证书过期日期
            
        Raises:
            Exception: 获取过期日期失败
        """
        cert_file = f'{cert_path}/cert.pem'
        if not os.path.exists(cert_file):
            raise Exception(f"Certificate file not found: {cert_file}")
        
        cmd = ['openssl', 'x509', '-enddate', '-noout', '-in', cert_file]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            date_str = result.stdout.split('=')[1].strip()
            return datetime.strptime(date_str, '%b %d %H:%M:%S %Y %Z')
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to get expiry date: {str(e.stderr)}")
            raise Exception(f"Failed to get expiry date: {str(e)}")
        except ValueError as e:
            logger.error(f"Failed to parse expiry date: {str(e)}")
            raise Exception(f"Failed to parse expiry date: {str(e)}")
    
    def renew_cert(self, cert_id: int, user) -> Certificate:
        """
        续期证书
        
        Args:
            cert_id: 证书ID
            user: 当前用户对象
            
        Returns:
            Certificate: 续期后的证书对象
            
        Raises:
            ValueError: 参数验证失败
            Exception: 证书续期失败
        """
        # 参数验证
        if not cert_id:
            raise ValueError("Certificate ID is required")
        
        if not user:
            raise ValueError("User is required")
        
        # 获取证书
        cert = Certificate.query.filter_by(id=cert_id, user_id=user.id).first()
        if not cert:
            raise Exception("Certificate not found or access denied")
        
        # 获取主域名作为证书名称
        main_domain = cert.domains.split(',')[0].strip()
        
        cmd = [
            'certbot', 'renew', '--non-interactive',
            '--cert-name', main_domain,
            '--config-dir', current_app.config['CERTBOT_CONFIG_DIR'],
            '--work-dir', current_app.config['CERTBOT_WORK_DIR'],
            '--logs-dir', current_app.config['CERTBOT_LOG_DIR']
        ]
        
        try:
            logger.info(f"Renewing certificate for domains: {cert.domains}")
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            cert.expiry_date = self._get_expiry_date(cert.cert_path)
            cert.payment_status = 'paid'
            db.session.commit()
            logger.info(f"Certificate renewed successfully for domains: {cert.domains}")
            return cert
        except subprocess.CalledProcessError as e:
            logger.error(f"Certificate renewal failed: {str(e.stderr)}")
            raise Exception(f"Certificate renewal failed: {str(e)}")
        except Exception as e:
            logger.error(f"Failed to renew certificate: {str(e)}")
            db.session.rollback()
            raise Exception(f"Failed to renew certificate: {str(e)}")
    
    def get_user_certs(self, user_id: int) -> List[Certificate]:
        """
        获取用户的所有证书
        
        Args:
            user_id: 用户ID
            
        Returns:
            List[Certificate]: 证书列表
        """
        return Certificate.query.filter_by(user_id=user_id).all()
    
    def get_cert_by_id(self, cert_id: int, user_id: int) -> Optional[Certificate]:
        """
        根据ID获取证书
        
        Args:
            cert_id: 证书ID
            user_id: 用户ID
            
        Returns:
            Optional[Certificate]: 证书对象，如果不存在则返回None
        """
        return Certificate.query.filter_by(id=cert_id, user_id=user_id).first()