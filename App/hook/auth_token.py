import json
from datetime import datetime, timedelta

from flask import current_app, request, url_for, g

from App.config import redis, db
from App.model import TokenInfo, RespModel, ProxyInfo, AccessInfo
from App.tool import BanBot


def get_admin_token():
    try:
        with open("App/resources/config.json") as f:
            json_dict = json.load(f)
            return json_dict.get("auth", {}).get("admin_token", "ezio911")
    except (FileNotFoundError, json.JSONDecodeError):
        return "ezio911"


def get_interval():
    try:
        with open("App/resources/config.json") as f:
            json_dict = json.load(f)
            return json_dict.get("crawl", {}).get("interval", 6)
    except (FileNotFoundError, json.JSONDecodeError):
        return 6


def get_and_update_proxy_info():
    six_hours_ago = datetime.utcnow() - timedelta(hours=get_interval())
    proxy = ProxyInfo.query.filter(
        ProxyInfo.is_used == 1,
        ProxyInfo.create_time >= six_hours_ago
    ).first()

    if proxy:
        proxy.is_used = 0
        db.session.commit()
        return proxy.proxy_info
    return RespModel(200, "管理员你好,数据库无任何可用代理信息").json_str


def setup_hooks():
    def check_ban(user_ip):
        bot = BanBot()
        return RespModel(403, "你已经被禁止访问!", data={"ip": user_ip}).json_str if bot.is_ban(user_ip) else None

    def check_token():
        unknown_token = request.args.get("token")
        if unknown_token == get_admin_token():
            return get_and_update_proxy_info()

        if TokenInfo.query.filter_by(token_info=unknown_token).first():
            return redis.get(unknown_token) or None
        return 401

    @current_app.before_request
    def handler_before_request():
        user_ip = request.remote_addr
        if (ban_resp := check_ban(user_ip)):
            return ban_resp

        if request.path == url_for("sub.get_proxy_info"):
            token_resp = check_token()
            if token_resp is None:
                return
            elif token_resp != 401:
                return token_resp
            else:
                BanBot().ban_ip(user_ip)
                return RespModel(401, "无效token").json_str

        if request.path in [url_for("sub.crawl_proxy_info"),
                            url_for("sub.del_ordinary_token"),
                            url_for("token.save_token")]:
            if request.args.get("token") != get_admin_token():
                BanBot().ban_ip(user_ip)
                return RespModel(401, "无效token").json_str

        if request.path == url_for("sub.get_sub_txt") and not TokenInfo.query.filter_by(
                token_info=request.args.get("token")).first():
            return RespModel(401, "无效token").json_str

    @current_app.teardown_request
    def handler_teardown_request(response):
        if request.path == url_for("sub.get_proxy_info"):
            access_info = AccessInfo()
            access_info.ip = request.remote_addr

            # 获取 g 中存储的 proxy_info
            proxy_info = getattr(g, 'proxy_info', '')
            if proxy_info:
                access_info.proxy_info = proxy_info
                db.session.add(access_info)
                db.session.commit()
        return response
