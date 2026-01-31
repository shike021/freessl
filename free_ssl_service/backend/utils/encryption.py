from cryptography.fernet import Fernet
from flask import current_app
import base64

class EncryptionService:
    @staticmethod
    def get_cipher():
        """
        获取加密器
        """
        key = current_app.config['ENCRYPTION_KEY']
        # 确保密钥是32字节
        if len(key.encode()) < 32:
            key = key.ljust(32, '0')
        elif len(key.encode()) > 32:
            key = key[:32]
        
        # 将密钥转换为Fernet兼容的格式
        key_bytes = key.encode()
        key_base64 = base64.urlsafe_b64encode(key_bytes)
        return Fernet(key_base64)
    
    @staticmethod
    def encrypt(data):
        """
        加密数据
        """
        if not data:
            return None
        cipher = EncryptionService.get_cipher()
        encrypted = cipher.encrypt(data.encode())
        return encrypted.decode()
    
    @staticmethod
    def decrypt(encrypted_data):
        """
        解密数据
        """
        if not encrypted_data:
            return None
        cipher = EncryptionService.get_cipher()
        decrypted = cipher.decrypt(encrypted_data.encode())
        return decrypted.decode()