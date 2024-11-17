import unittest

from .. import create_app
from ..config import db
from ..model.sub_model import ProxyInfo


class TestSubModel(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        # 设置测试专用数据库
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///FreeNodeTest.db"
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        self.app.testing = True

        # 在应用上下文中创建所有表
        with self.app.app_context():
            db.create_all()

    def test_add_proxyInfo(self):
        with self.app.app_context():
            info = ProxyInfo(proxy_info="123456")
            db.session.add(info)
            db.session.commit()

            info = db.session.query(ProxyInfo).filter_by(proxy_info="123456").first()
            self.assertEqual(info.proxy_info, "123456")

    def tearDown(self):
        # 测试完成后删除所有数据和表
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
