import tls_client

from identity_pool.proxy_manager import build_proxy

class Identity:

    def __init__(self, name, cookies=None):
        self.name = name

        self.session = tls_client.Session(
            client_identifier="chrome_120",
            random_tls_extension_order=True
        )

        # attach sticky proxy
        proxy = build_proxy(name)
        if proxy:
            self.session.proxies = proxy


        if cookies:
            for k, v in cookies.items():
                self.session.cookies.set(k, v)
