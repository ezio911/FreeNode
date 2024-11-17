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


class SubTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True  # 开启测试模式,显示错误细节
        self.client = self.app.test_client()
        self.admin_token = get_admin_token()

    def test_get_with_admin_token(self):
        """
        token获取代理信息
        :return:
        """
        # 1.管理员token获取代理信息
        resp = self.client.get(f"/sub/get?token={self.admin_token}").data
        self.assertTrue(resp)

        # 普通token获取代理信息
        resp = self.client.get(f"/sub/get?token=1731566178").data
        self.assertTrue(resp)

    def test_get_with_error_token(self):
        """
        测试用错误的token 3次请求后返回403
        :return:
        """
        # 前 3 次请求预期为 401
        for _ in range(3):
            resp = self.client.get("/sub/get?token=1111").data
            resp = json.loads(resp.decode("utf-8"))
            self.assertEqual(resp["code"], 401)

        # 第 4 次请求预期为 403
        resp = self.client.get("/sub/get?token=1111").data
        resp = json.loads(resp.decode("utf-8"))
        self.assertEqual(resp["code"], 403)

    def test_qrcode_with_error_token(self):
        """
        管理员或者错误token不允许生成二维码,返回401
        :return:
        """
        resp = self.client.get(f"/sub/qrcode?token={self.admin_token}").data
        resp = json.loads(resp.decode("utf-8"))
        self.assertEqual(resp["code"], 401)

        resp = self.client.get(f"/sub/qrcode?token=xxxx").data
        resp = json.loads(resp.decode("utf-8"))
        self.assertEqual(resp["code"], 401)

    def test_qrcode_with_general_token(self):
        """
        普通token的允许生成二维码
        :return:
        """
        resp = self.client.get(f"/sub/qrcode?token=123").data
        self.assertTrue(resp)

    def test_del_with_admin_token(self):
        """
        删除普通用户的token
        :return:
        """
        user_token = 456  # 这是一个数据库存在的普通token
        url = f"/sub/del?token={self.admin_token}&user_token={user_token}"
        resp = self.client.get(url).data
        resp = json.loads(resp.decode("utf-8"))
        self.assertEqual(resp["code"], 200)

        # # 因为已经被上一步删除,所以这一步返回210,表示数据库没有这个token
        resp = self.client.get(f"/sub/del?token={self.admin_token}&user_token={user_token}").data
        resp = json.loads(resp.decode("utf-8"))
        self.assertEqual(resp["code"], 210)

    def test_crawl_with_admin_token(self):
        """
        测试爬取代理信息,会自动删除配置文件设定的超过一定时间的代理信息,然后爬取
        :return:
        """
        resp = self.client.get(f"/sub/crawl?token={self.admin_token}").data
        resp = json.loads(resp.decode("utf-8"))
        self.assertEqual(resp["code"], 200)


if __name__ == '__main__':
    unittest.main()
