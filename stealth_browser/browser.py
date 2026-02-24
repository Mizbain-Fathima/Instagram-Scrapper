import undetected_chromedriver as uc
import os

PROFILE_PATH = os.path.join(os.getcwd(), "ig_profile")

def create_browser(headless=False):

    options = uc.ChromeOptions()

    if headless:
        options.add_argument("--headless=new")

    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = uc.Chrome(options=options)
    return driver