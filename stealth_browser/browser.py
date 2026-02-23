import undetected_chromedriver as uc
import os

PROFILE_PATH = os.path.join(os.getcwd(), "ig_profile")

def create_browser():

    options = uc.ChromeOptions()

    # persistent real browser identity
    options.add_argument(f"--user-data-dir={PROFILE_PATH}")
    options.add_argument("--profile-directory=Default")

    # stealth flags
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")

    driver = uc.Chrome(options=options, headless=False)
    return driver