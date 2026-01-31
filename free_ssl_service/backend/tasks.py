from celery.schedules import crontab
from app import celery
from models.cert_model import Certificate, db
from models.user_model import User
from services.email_service import EmailService
from datetime import datetime, timedelta

@celery.task
def check_certificate_expiry():
    """
    检查证书到期情况并发送提醒邮件
    """
    now = datetime.now()
    
    # 检查30天内到期的证书
    thirty_days_from_now = now + timedelta(days=30)
    expiring_certs = Certificate.query.filter(
        Certificate.expiry_date <= thirty_days_from_now,
        Certificate.expiry_date > now,
        Certificate.notified_free_expiry == False
    ).all()
    
    for cert in expiring_certs:
        try:
            user = User.query.get(cert.user_id)
            if user:
                EmailService.send_certificate_expiry_notification(user, cert)
                cert.notified_free_expiry = True
                db.session.commit()
        except Exception as e:
            print(f"Failed to send expiry notification for cert {cert.id}: {str(e)}")
            db.session.rollback()
    
    return f"Checked {len(expiring_certs)} expiring certificates"

@celery.task
def check_free_expiry():
    """
    检查免费期即将结束的证书并发送提醒
    """
    now = datetime.now()
    
    # 检查免费期在30天内结束的证书
    thirty_days_from_now = now + timedelta(days=30)
    free_expiry_certs = Certificate.query.filter(
        Certificate.free_expiry_date <= thirty_days_from_now,
        Certificate.free_expiry_date > now,
        Certificate.payment_status == 'free'
    ).all()
    
    for cert in free_expiry_certs:
        try:
            user = User.query.get(cert.user_id)
            if user:
                EmailService.send_free_expiry_notification(user, cert)
        except Exception as e:
            print(f"Failed to send free expiry notification for cert {cert.id}: {str(e)}")
    
    return f"Checked {len(free_expiry_certs)} certificates with free expiry"

@celery.task
def auto_renew_certificates():
    """
    自动续期已付费的证书
    """
    now = datetime.now()
    
    # 查找30天内到期的已付费证书
    thirty_days_from_now = now + timedelta(days=30)
    paid_certs_to_renew = Certificate.query.filter(
        Certificate.expiry_date <= thirty_days_from_now,
        Certificate.expiry_date > now,
        Certificate.payment_status == 'paid'
    ).all()
    
    renewed_count = 0
    for cert in paid_certs_to_renew:
        try:
            from services.cert_service import CertService
            user = User.query.get(cert.user_id)
            if user:
                cert_service = CertService()
                cert_service.renew_cert(cert.id, user)
                renewed_count += 1
        except Exception as e:
            print(f"Failed to auto-renew cert {cert.id}: {str(e)}")
    
    return f"Auto-renewed {renewed_count} certificates"

# Celery Beat schedule configuration
celery.conf.beat_schedule = {
    'check-certificate-expiry-daily': {
        'task': 'tasks.check_certificate_expiry',
        'schedule': crontab(hour=9, minute=0),  # 每天上午9点执行
    },
    'check-free-expiry-daily': {
        'task': 'tasks.check_free_expiry',
        'schedule': crontab(hour=9, minute=30),  # 每天上午9:30执行
    },
    'auto-renew-certificates-daily': {
        'task': 'tasks.auto_renew_certificates',
        'schedule': crontab(hour=10, minute=0),  # 每天上午10点执行
    },
}