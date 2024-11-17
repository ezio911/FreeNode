from App.config import redis
import json


class BanBot:
    def __init__(self):
        self.try_count = 3
        self.ban_duration = 3600

        try:
            with open("App/resources/config.json", "r") as f:
                json_dict = json.load(f)
                # 如果文件中存在相应的值，更新自定义的 try_count 和 ban_duration
                self.try_count = json_dict.get("banBot", {}).get("try_count", self.try_count)
                self.ban_duration = json_dict.get("banBot", {}).get("ban_duration", self.ban_duration)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"配置文件加载失败: {e}. 使用默认值.")

    # 查询 IP 是否被封禁
    def is_ban(self, ip):
        """
        :param ip: remote_addr
        :return: True if banned
        """
        result = redis.get(ip)
        if result and int(result) >= self.try_count:
            return True
        return False

    # 记录 ip 校验失败次数并进行封禁处理
    def ban_ip(self, ip):
        """
        记录 IP 校验失败的次数
        :param ip: IP 地址
        :return: None
        """
        current_count = redis.incr(ip)  # 失败次数递增
        if current_count == 1:
            # 设置初次封禁时间
            redis.expire(ip, self.ban_duration)  # 设置过期时间
        if current_count >= self.try_count:
            # 达到封禁次数，封禁该 IP
            redis.setex(ip, self.ban_duration, current_count)


__all__ = ["BanBot"]
