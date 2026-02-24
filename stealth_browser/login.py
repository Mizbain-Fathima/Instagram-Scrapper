from .browser import create_browser
from .cookie_store import save_cookies

driver = create_browser()
driver.get("https://www.instagram.com/")

input("🔐 Login manually then press ENTER...")

save_cookies(driver)
print("✅ Session saved successfully.")