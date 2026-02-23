from identity_pool.proxy_validator import is_proxy_alive

def get_proxy(index):

    for _ in range(5):  # try 5 proxies

        proxy = PROXIES[index % len(PROXIES)]

        if is_proxy_alive(proxy):
            return proxy

        print("Dead proxy removed:", proxy)
        index += 1

    raise Exception("No working proxies available")

def build_proxy(identity_name):
    # TEMP: no proxy (direct connection)
    return None
