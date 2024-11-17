from flask import Blueprint, request, current_app, g
from sqlalchemy.exc import SQLAlchemyError
from App.config import cache, db, redis
from App.model import ProxyInfo, RespModel, TokenInfo
from App.tool import get_nodes, str_to_qrcode
import json
from threading import Thread, Lock
from datetime import datetime, timedelta
from sqlalchemy import and_

sub = Blueprint("sub", __name__)
total = 10
interval = 6
config_lock = Lock()
CRAWL_STATUS = True


def load_config():
    global total, interval
    try:
        with open("App/resources/config.json") as f:
            json_dict = json.load(f)
            total = json_dict.get("crawl", {}).get("total", total)
            interval = json_dict.get("crawl", {}).get("interval", interval)
    except (FileNotFoundError, json.JSONDecodeError):
        pass


load_config()


@sub.route("/get")
def get_proxy_info():
    token = request.args.get("token")
    proxy_info = get_nodes()
    if proxy_info:
        try:
            redis.setex(token, 3600 * interval, proxy_info)
            new_info = ProxyInfo(proxy_info=proxy_info, is_used=0)
            db.session.add(new_info)
            db.session.commit()
            # 保存这个值,传递给钩子函数
            g.proxy_info = proxy_info
            return proxy_info
        except SQLAlchemyError:
            db.session.rollback()
            return RespModel(500, "数据库错误，请稍后重试").json_str
        except Exception as e:
            return RespModel(500, f"发生错误: {str(e)}").json_str
    else:
        return RespModel(502, "服务器正忙，请稍候重试").json_str


@sub.route("/qrcode")
@cache.cached(timeout=100)
def get_sub_txt():
    return str_to_qrcode(request.url)


@sub.route("/del")
def del_ordinary_token():
    user_token = request.args.get("user_token", None)
    try:
        token_info = TokenInfo.query.filter_by(token_info=user_token).first()
        if token_info:
            db.session.delete(token_info)
            db.session.commit()
            return RespModel(200, "Token 信息删除成功").json_str
        else:
            return RespModel(210, "未找到该 Token 信息").json_str
    except Exception as e:
        db.session.rollback()
        return RespModel(500, f"发生错误: {str(e)}").json_str


@sub.route("/crawl")
def crawl_proxy_info():
    Thread(target=crawl_task, args=(current_app._get_current_object(),)).start()
    return RespModel(200, "正在爬取,请稍后...").json_str


def crawl_task(app):
    with app.app_context():
        with config_lock:
            current_time = datetime.utcnow()
            time_period = current_time - timedelta(hours=interval)

            ProxyInfo.query.filter(
                and_(
                    ProxyInfo.is_used == 0,
                    ProxyInfo.create_time < time_period
                )
            ).delete(synchronize_session=False)

            new_proxies = [ProxyInfo(proxy_info=get_nodes()) for _ in range(total)]
            db.session.bulk_save_objects(new_proxies)
            db.session.commit()


__all__ = ["sub"]
