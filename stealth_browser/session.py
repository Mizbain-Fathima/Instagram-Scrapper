from .browser import create_browser
from .cookie_store import load_cookies

# stealth_browser/session.py

_driver = None

def get_session(headless=False):
    global _driver

    if _driver is None:
        from .browser import create_browser
        from .cookie_store import load_cookies

        print("🌐 Creating persistent browser session...")

        _driver = create_browser(headless=headless)
        _driver.get("https://www.instagram.com/")

        load_cookies(_driver)
        _driver.refresh()

    return _driver