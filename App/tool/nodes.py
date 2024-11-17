import requests
import re
import base64
from fake_useragent import UserAgent


def get_nodes() -> str | None:
    """
    获取网络代理信息
    :return:
    """
    headers = {
        "User-Agent": UserAgent().random
    }
    session = requests.Session()

    try:
        resp = session.get("https://getafreenode.com/", headers=headers).text
        uuid_match = re.search(r'uuid=(.*?)"', resp)
        if not uuid_match:
            print("UUID 未找到")
            return None
        uuid = uuid_match.group(1)

        session.get(f"https://getafreenode.com/node.php?uuid={uuid}", headers=headers)
        b64_result = session.get(f"https://getafreenode.com/subscribe/?uuid={uuid}", headers=headers).text

        padded_b64_result = b64_result + '=' * (-len(b64_result) % 4)
        decoded_result = base64.b64decode(padded_b64_result).decode("utf-8").strip()
        nodes_encoded = base64.b64encode(decoded_result.encode()).decode("utf-8")
        return nodes_encoded

    except (requests.RequestException, base64.binascii.Error) as e:
        print("Error:", e)
        return None


__all__ = ["get_nodes"]
