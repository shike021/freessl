import uuid
from flask import current_app
from models.payment_model import PaymentOrder, db
from datetime import datetime

class PaymentService:
    @staticmethod
    def create_order(user_id, cert_id, amount, payment_method):
        """
        创建支付订单
        """
        order_id = str(uuid.uuid4())
        
        order = PaymentOrder(
            order_id=order_id,
            user_id=user_id,
            cert_id=cert_id,
            amount=amount,
            payment_method=payment_method,
            status='pending'
        )
        db.session.add(order)
        db.session.commit()
        
        return order
    
    @staticmethod
    def get_alipay_payment_url(order):
        """
        获取支付宝支付URL
        """
        # 这里需要集成支付宝SDK
        # 示例代码，实际使用时需要替换为真实的支付宝SDK调用
        alipay_gateway = "https://openapi.alipay.com/gateway.do"
        
        params = {
            'app_id': current_app.config.get('ALIPAY_APP_ID'),
            'method': 'alipay.trade.page.pay',
            'charset': 'utf-8',
            'sign_type': 'RSA2',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'version': '1.0',
            'out_trade_no': order.order_id,
            'total_amount': str(order.amount),
            'subject': f'SSL证书续期 - {order.certificate.domains}',
            'product_code': 'FAST_INSTANT_TRADE_PAY',
            'return_url': f"{current_app.config.get('FRONTEND_URL')}/payment/return",
            'notify_url': f"{current_app.config.get('BACKEND_URL')}/api/payment/alipay/notify"
        }
        
        # 实际使用时需要调用支付宝SDK生成签名和支付URL
        # 这里返回示例URL
        return f"{alipay_gateway}?out_trade_no={order.order_id}&total_amount={order.amount}"
    
    @staticmethod
    def get_wechat_payment_url(order):
        """
        获取微信支付URL
        """
        # 这里需要集成微信支付SDK
        # 示例代码，实际使用时需要替换为真实的微信支付SDK调用
        wechat_gateway = "https://api.mch.weixin.qq.com/pay/unifiedorder"
        
        params = {
            'appid': current_app.config.get('WECHAT_PAY_APP_ID'),
            'mch_id': current_app.config.get('WECHAT_PAY_MCH_ID'),
            'nonce_str': str(uuid.uuid4()),
            'body': f'SSL证书续期 - {order.certificate.domains}',
            'out_trade_no': order.order_id,
            'total_fee': int(order.amount * 100),  # 微信支付金额单位为分
            'spbill_create_ip': '127.0.0.1',
            'notify_url': f"{current_app.config.get('BACKEND_URL')}/api/payment/wechat/notify",
            'trade_type': 'NATIVE'
        }
        
        # 实际使用时需要调用微信支付SDK生成支付二维码
        # 这里返回示例URL
        return f"weixin://wxpay/bizpayurl?pr={order.order_id}"
    
    @staticmethod
    def verify_alipay_notification(data):
        """
        验证支付宝支付回调
        """
        # 实际使用时需要调用支付宝SDK验证签名
        order_id = data.get('out_trade_no')
        trade_status = data.get('trade_status')
        
        if trade_status == 'TRADE_SUCCESS' or trade_status == 'TRADE_FINISHED':
            order = PaymentOrder.query.filter_by(order_id=order_id).first()
            if order and order.status == 'pending':
                order.status = 'paid'
                order.paid_at = datetime.now()
                order.transaction_id = data.get('trade_no')
                
                # 更新证书支付状态
                order.certificate.payment_status = 'paid'
                db.session.commit()
                
                return True
        
        return False
    
    @staticmethod
    def verify_wechat_notification(data):
        """
        验证微信支付回调
        """
        # 实际使用时需要调用微信支付SDK验证签名
        order_id = data.get('out_trade_no')
        return_code = data.get('return_code')
        
        if return_code == 'SUCCESS' and data.get('result_code') == 'SUCCESS':
            order = PaymentOrder.query.filter_by(order_id=order_id).first()
            if order and order.status == 'pending':
                order.status = 'paid'
                order.paid_at = datetime.now()
                order.transaction_id = data.get('transaction_id')
                
                # 更新证书支付状态
                order.certificate.payment_status = 'paid'
                db.session.commit()
                
                return True
        
        return False