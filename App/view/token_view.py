import json

from flask import Blueprint, request

from App.config import db
from App.model import RespModel, TokenInfo

token = Blueprint("token", __name__)


def get_admin_token():
    try:
        with open("App/resources/config.json", "r") as f:
            json_dict = json.load(f)
            return json_dict.get("auth", {}).get("admin_token", "ezio911")
    except (FileNotFoundError, json.JSONDecodeError):
        return "ezio911"


@token.route("/create")
def save_token():
    user_token = request.args.get("user_token")
    if user_token is None:
        return RespModel(210, msg="user_token为必传参数").json_str
    result = TokenInfo.query.filter_by(token_info=user_token).first()
    if result is None:
        new_token = TokenInfo(token_info=user_token)
        db.session.add(new_token)
        db.session.commit()
        return RespModel(200, msg="保存token成功", data={"token": user_token}).json_str
    else:
        return RespModel(210, "已存在该token!", data={"token": user_token}).json_str


__all__ = ["token"]
