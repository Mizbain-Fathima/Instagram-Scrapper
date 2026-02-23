import json
import os

COOKIE_FILE = "stealth_browser/session_cookies.json"


def save_cookies(driver):
    """Save cookies after manual login"""
    cookies = driver.get_cookies()

    os.makedirs("stealth_browser", exist_ok=True)

    with open(COOKIE_FILE, "w", encoding="utf-8") as f:
        json.dump(cookies, f, indent=2)

    print("💾 Cookies saved:", COOKIE_FILE)


def load_cookies(driver):
    """Load cookies before scraping"""

    if not os.path.exists(COOKIE_FILE):
        print("⚠ No saved session. Run login first.")
        return False

    with open(COOKIE_FILE, "r", encoding="utf-8") as f:
        cookies = json.load(f)

    for cookie in cookies:
        cookie.pop("sameSite", None)  # selenium fix
        try:
            driver.add_cookie(cookie)
        except Exception:
            pass

    print("🍪 Cookies loaded")
    return True