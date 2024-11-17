import time
import unittest
from .. import create_app
import json


def get_admin_token():
    try:
        with open("App/resources/config.json") as f:
            json_dict = json.load(f)
            return json_dict.get("auth", {}).get("admin_token", "ezio911")
    except (FileNotFoundError, json.JSONDecodeError):
        return "ezio911"


class TestToken(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()
        self.admin_token = get_admin_token()

    def test_create_with_admin_token(self):
        # 1.管理员token正确,不传用户token
        url = f"/token/create?token={self.admin_token}"
        resp = self.client.get(url).data
        resp = json.loads(resp.decode("utf-8"))
        self.assertEqual(resp["code"], 210)

        # 2.管理员token正确,传入不存在token
        user_token = int(time.time())
        url = f"/token/create?token={self.admin_token}&user_token={user_token}"
        resp = self.client.get(url).data
        resp = json.loads(resp.decode("utf-8"))
        self.assertEqual(resp["code"], 200)

        # 3.管理员token正确,传入已经存在token
        url = f"/token/create?token={self.admin_token}&user_token={user_token}"
        resp = self.client.get(url).data
        resp = json.loads(resp.decode("utf-8"))
        self.assertEqual(resp["code"], 210)

        # 4.传入错误的管理员token正确,传入已经存在token
        url = f"/token/create?token=xxxxx&user_token={user_token}"
        resp = self.client.get(url).data
        resp = json.loads(resp.decode("utf-8"))
        self.assertEqual(resp["code"], 401)
