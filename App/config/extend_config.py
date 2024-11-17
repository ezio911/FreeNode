from flask_caching import Cache
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy

redis = FlaskRedis(config_prefix="REDIS")
cache = Cache()
db = SQLAlchemy()


def init_extends(app):
    redis.init_app(app=app)
    cache.init_app(app, config={
        "CACHE_TYPE": "redis",
        "CACHE_REDIS_URL": app.config["REDIS_URL"]
    })
    db.init_app(app)


__all__ = ["init_extends", "cache", "redis","db"]
