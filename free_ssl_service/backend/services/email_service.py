from flask import current_app
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os

class EmailService:
    @staticmethod
    def _get_smtp_connection():
        smtp_host = current_app.config.get('SMTP_HOST', 'smtp.gmail.com')
        smtp_port = current_app.config.get('SMTP_PORT', 587)
        smtp_user = current_app.config.get('SMTP_USER', '')
        smtp_password = current_app.config.get('SMTP_PASSWORD', '')

        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        return server

    @staticmethod
    def _send_email(to_email, subject, html_content):
        smtp_user = current_app.config.get('SMTP_USER', '')
        from_email = current_app.config.get('EMAIL_FROM', smtp_user)

        message = MIMEMultipart('alternative')
        message['From'] = from_email
        message['To'] = to_email
        message['Subject'] = subject

        part = MIMEText(html_content, 'html')
        message.attach(part)

        try:
            server = EmailService._get_smtp_connection()
            server.sendmail(from_email, [to_email], message.as_string())
            server.quit()
            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            raise Exception(f"Failed to send email: {str(e)}")

    @staticmethod
    def _get_base_url():
        return current_app.config.get('EMAIL_BASE_URL', 'http://localhost:8080')

    @staticmethod
    def send_verification_email(user):
        base_url = EmailService._get_base_url()
        verification_url = f"{base_url}/verify/{user.verification_token}"

        html_content = f'''
        <html>
            <body>
                <h2>欢迎加入Free SSL服务</h2>
                <p>您好 {user.username},</p>
                <p>感谢您注册我们的服务。请点击下面的链接验证您的账户：</p>
                <p><a href="{verification_url}">验证账户</a></p>
                <p>如果您没有注册此账户，请忽略此邮件。</p>
                <p>此链接将在24小时后过期。</p>
                <p>祝好，<br>Free SSL团队</p>
            </body>
        </html>
        '''

        try:
            EmailService._send_email(user.email, '验证您的账户', html_content)
            return True
        except Exception as e:
            print(f"Failed to send verification email: {str(e)}")
            raise Exception("Failed to send verification email")

    @staticmethod
    def send_password_reset_email(user, reset_token):
        base_url = EmailService._get_base_url()
        reset_url = f"{base_url}/reset-password?token={reset_token}"

        html_content = f'''
        <html>
            <body>
                <h2>重置密码</h2>
                <p>您好 {user.username},</p>
                <p>我们收到了重置您账户密码的请求。</p>
                <p>请点击下面的链接重置您的密码：</p>
                <p><a href="{reset_url}">重置密码</a></p>
                <p>如果您没有请求重置密码，请忽略此邮件。</p>
                <p>此链接将在1小时后过期。</p>
                <p>祝好，<br>Free SSL团队</p>
            </body>
        </html>
        '''

        try:
            EmailService._send_email(user.email, '重置您的密码', html_content)
            return True
        except Exception as e:
            print(f"Failed to send password reset email: {str(e)}")
            raise Exception("Failed to send password reset email")

    @staticmethod
    def send_certificate_expiry_notification(user, cert):
        base_url = EmailService._get_base_url()
        days_until_expiry = (cert.expiry_date - cert.free_expiry_date).days

        html_content = f'''
        <html>
            <body>
                <h2>证书即将到期提醒</h2>
                <p>您好 {user.username},</p>
                <p>您的SSL证书即将到期：</p>
                <ul>
                    <li><strong>域名：</strong>{cert.domains}</li>
                    <li><strong>到期日期：</strong>{cert.expiry_date.strftime('%Y-%m-%d')}</li>
                    <li><strong>剩余天数：</strong>{days_until_expiry}天</li>
                </ul>
                <p>请注意，免费期将在 {cert.free_expiry_date.strftime('%Y-%m-%d')} 结束。</p>
                <p>如需续期，请登录您的账户并选择付费续期选项。</p>
                <p><a href="{base_url}/certificates">查看我的证书</a></p>
                <p>祝好，<br>Free SSL团队</p>
            </body>
        </html>
        '''

        try:
            EmailService._send_email(user.email, f'证书即将到期提醒 - {cert.domains}', html_content)
            return True
        except Exception as e:
            print(f"Failed to send expiry notification email: {str(e)}")
            raise Exception("Failed to send expiry notification email")

    @staticmethod
    def send_free_expiry_notification(user, cert):
        base_url = EmailService._get_base_url()

        html_content = f'''
        <html>
            <body>
                <h2>免费期即将结束提醒</h2>
                <p>您好 {user.username},</p>
                <p>您的SSL证书免费期即将结束：</p>
                <ul>
                    <li><strong>域名：</strong>{cert.domains}</li>
                    <li><strong>免费期结束日期：</strong>{cert.free_expiry_date.strftime('%Y-%m-%d')}</li>
                    <li><strong>证书到期日期：</strong>{cert.expiry_date.strftime('%Y-%m-%d')}</li>
                </ul>
                <p>免费期结束后，如需继续使用SSL证书，请选择付费续期选项。</p>
                <p><a href="{base_url}/certificates/{cert.id}/renew">续期证书</a></p>
                <p>祝好，<br>Free SSL团队</p>
            </body>
        </html>
        '''

        try:
            EmailService._send_email(user.email, f'免费期即将结束提醒 - {cert.domains}', html_content)
            return True
        except Exception as e:
            print(f"Failed to send free expiry notification email: {str(e)}")
            raise Exception("Failed to send free expiry notification email")