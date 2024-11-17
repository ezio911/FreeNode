from App.config import db


class ProxyInfo(db.Model):
    """
    服务器获取到的代理信息
    """
    __tablename__ = 'proxy_info'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    proxy_info = db.Column(db.String, nullable=False)
    create_time = db.Column(db.String, default=db.func.current_timestamp(), nullable=False)
    is_used = db.Column(db.Integer, default=1, nullable=False)
