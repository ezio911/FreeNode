import json
import os

redis_host = os.getenv("REDIS_HOST", "free-node-redis")
redis_port = os.getenv("REDIS_PORT", "6379")
redis_password = os.getenv("REDIS_PWD", None)

def load_config():
    global redis_host, redis_port, redis_password
    try:
        with open("App/resources/config.json") as f:
            json_dict = json.load(f)
            redis_host = json_dict.get("redis", {}).get("host", redis_host)
            redis_port = json_dict.get("redis", {}).get("port", redis_port)
            redis_password = json_dict.get("redis", {}).get("password", redis_password)
    except (FileNotFoundError, json.JSONDecodeError):
        pass


class SqliteSettings(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///FreeNode.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class RedisSettings(object):
    load_config()
    if redis_password:
        REDIS_URL = f"redis://:{redis_password}@{redis_host}:{redis_port}/0"
    else:
        REDIS_URL = f"redis://{redis_host}:{redis_port}/0"

    REDIS_POOL = {
        'max_connections': 10,
        'timeout': 5,
        'retry_on_timeout': True,
    }


__all__ = ["SqliteSettings", "RedisSettings"]
