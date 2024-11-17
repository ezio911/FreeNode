from flask import Flask

from App.config import SqliteSettings, RedisSettings, init_extends, db
from App.view import sub, token, handler_error
from App.hook import setup_hooks
from App.model import ProxyInfo, AccessInfo


def create_app():
    app = Flask(__name__)

    # 加载各种配置文件,如数据库,定时任务配置...
    app.config.from_object(SqliteSettings)
    app.config.from_object(RedisSettings)

    # 加载第三方插件 flask-cache,flask-redis,flask-SQLAlchemy...
    init_extends(app)

    # 注册蓝图
    app.register_blueprint(sub, url_prefix="/sub")
    app.register_blueprint(token, url_prefix="/token")
    app.register_blueprint(handler_error)

    # 确保在应用上下文中执行
    with app.app_context():
        setup_hooks()  # 添加钩子
        db.create_all()  # 创建数据库表

    return app
