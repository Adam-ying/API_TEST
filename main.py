from datetime import datetime

import requests
import json

from Common.http_client import HttpClient
from Util.tools import time_diff_stamp


def feishu_post_test():
    msg = {
        "msg_type": "text",
        "content": {"text": "你好"}
    }

    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/cb8d22de-6f35-4858-bb82-593f19055780"

    headers = {
        "Content-type": "application/json",
        "charset": "utf-8"
    }

    msg_encode = json.dumps(msg, ensure_ascii=True).encode("utf-8")
    reponse = requests.post(url=webhook_url, data=msg_encode, headers=headers)
    print(reponse)

def timestamp_test():
    timestamp1 = 1642387200  # 2022-01-17 00:00:00 UTC 的时间戳
    timestamp2 = 1642387232

    dt1 = datetime.fromtimestamp(timestamp1)

    dt2 = datetime.fromtimestamp(timestamp2)
    print(dt2 - dt1)


def get_token_test():
    hc = HttpClient()


if __name__ == '__main__':
    pass
