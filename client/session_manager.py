# session_manager.py

import requests
import json
import os
from config import BASE_HEADERS

COOKIE_FILE = "storage/cookie_store.json"

class SessionManager:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(BASE_HEADERS)
        self.load()

    def save(self):
        with open(COOKIE_FILE, "w") as f:
            json.dump(self.session.cookies.get_dict(), f)

    def load(self):
        if os.path.exists(COOKIE_FILE):
            with open(COOKIE_FILE, "r") as f:
                cookies = json.load(f)
                self.session.cookies.update(cookies)
