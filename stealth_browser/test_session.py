from .browser import create_browser
from .cookie_store import load_cookies

driver = create_browser()
load_cookies(driver)

driver.get("https://www.instagram.com/")

input("You should be logged in. Press enter to exit")
driver.quit()