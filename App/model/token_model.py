from App.config import db


class TokenInfo(db.Model):
    """
    普通token对象
    """
    __tablename__ = 'token_info'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token_info = db.Column(db.String, nullable=False)
    create_time = db.Column(db.String, default=db.func.current_timestamp(), nullable=False)
    is_used = db.Column(db.Integer, default=1, nullable=False)
