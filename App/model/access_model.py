from App.config import db


class AccessInfo(db.Model):
    """
    记录每一个ip请求成功后,获得代理的信息
    """
    __tablename__ = 'access_info'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String, nullable=False)
    proxy_info = db.Column(db.String, nullable=False)
    create_time = db.Column(db.String, default=db.func.current_timestamp(), nullable=False)
