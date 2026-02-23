import requests
import time

TEST_URL = "https://www.instagram.com/"
TIMEOUT = 8


def is_proxy_alive(proxy_url):

    try:
        proxies = {
            "http": proxy_url,
            "https": proxy_url
        }

        r = requests.get(TEST_URL, proxies=proxies, timeout=TIMEOUT)

        if r.status_code == 200 and len(r.text) > 50000:
            return True

        return False

    except Exception:
        return False