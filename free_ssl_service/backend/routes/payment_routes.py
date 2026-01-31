from flask import Blueprint, request, jsonify
from services.auth_service import AuthService
from services.payment_service import PaymentService
from models.payment_model import PaymentOrder
from datetime import datetime

payment_bp = Blueprint('payment', __name__, url_prefix='/api/payment')

@payment_bp.route('/create', methods=['POST'])
def create_payment():
    """
    创建支付订单
    """
    user = AuthService.get_current_user()
    data = request.json
    
    cert_id = data.get('cert_id')
    payment_method = data.get('payment_method')
    amount = data.get('amount', 99.00)  # 默认价格
    
    if not cert_id or not payment_method:
        return jsonify({'error': 'Missing required fields'}), 400
    
    if payment_method not in ['alipay', 'wechat']:
        return jsonify({'error': 'Invalid payment method'}), 400
    
    try:
        order = PaymentService.create_order(user.id, cert_id, amount, payment_method)
        
        if payment_method == 'alipay':
            payment_url = PaymentService.get_alipay_payment_url(order)
        else:
            payment_url = PaymentService.get_wechat_payment_url(order)
        
        return jsonify({
            'order_id': order.order_id,
            'payment_url': payment_url,
            'amount': float(order.amount)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@payment_bp.route('/alipay/notify', methods=['POST'])
def alipay_notify():
    """
    支付宝支付回调
    """
    try:
        if PaymentService.verify_alipay_notification(request.form):
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'failed'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@payment_bp.route('/wechat/notify', methods=['POST'])
def wechat_notify():
    """
    微信支付回调
    """
    try:
        import xml.etree.ElementTree as ET
        xml_data = request.data.decode('utf-8')
        root = ET.fromstring(xml_data)
        data = {child.tag: child.text for child in root}
        
        if PaymentService.verify_wechat_notification(data):
            return jsonify({'return_code': 'SUCCESS', 'return_msg': 'OK'})
        else:
            return jsonify({'return_code': 'FAIL', 'return_msg': 'Payment failed'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@payment_bp.route('/order/<order_id>', methods=['GET'])
def get_order(order_id):
    """
    获取订单状态
    """
    user = AuthService.get_current_user()
    order = PaymentOrder.query.filter_by(order_id=order_id, user_id=user.id).first()
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    return jsonify(order.to_dict())