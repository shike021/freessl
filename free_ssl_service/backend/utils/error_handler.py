from flask import jsonify
from werkzeug.exceptions import HTTPException
import traceback

def handle_error(error):
    """
    统一错误处理中间件
    """
    response = {
        'error': str(error)
    }
    
    if isinstance(error, HTTPException):
        response['error'] = error.description
        status_code = error.code
    else:
        response['error'] = 'Internal server error'
        status_code = 500
    
    # 在开发环境下打印错误堆栈
    import os
    if os.getenv('FLASK_ENV') == 'development':
        response['traceback'] = traceback.format_exc()
    
    return jsonify(response), status_code

def register_error_handlers(app):
    """
    注册所有错误处理器
    """
    app.register_error_handler(Exception, handle_error)
    app.register_error_handler(HTTPException, handle_error)