from flask import Blueprint

handler_error = Blueprint("handler_error_page", __name__)


@handler_error.app_errorhandler(404)
def handler_error_page(error_info):
    return "请求地址错误!"


@handler_error.app_errorhandler(500)
def handler_error_page(error_info):
    return "服务器内部错误,请通知管理员处理!"


__all__ = ["handler_error"]
