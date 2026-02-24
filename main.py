# main.py

import argparse
import re
from storage.storage import save_snapshot
from stealth_browser.session import get_session
from stealth_browser.profile_scraper import scrape_profile
from stealth_browser.post_scraper import scrape_post


# ---------------- HELPERS ----------------

def extract_shortcode(url):
    match = re.search(r"/p/([^/]+)/?", url)
    return match.group(1) if match else None


def load_urls_from_file(path):
    urls = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            urls.append(line)
    return urls


# ---------------- PROCESSOR ----------------

def process_url(url, driver):

    if "/p/" in url:
        shortcode = extract_shortcode(url)

        if not shortcode:
            print("❌ Invalid post URL:", url)
            return

        print(f"[STEALTH] Post → {shortcode}")

        result = scrape_post(shortcode, driver)

        result["type"] = "post"
        result["shortcode"] = shortcode
        result["url"] = url

    else:
        username = url.rstrip("/").split("/")[-1]

        print(f"[STEALTH] Profile → {username}")

        result = scrape_profile(username, driver)

        result["type"] = "profile"
        result["username"] = username
        result["url"] = url

    save_snapshot(result)


# ---------------- MAIN ----------------

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="Single URL")
    parser.add_argument("--file", help="File containing URLs")
    parser.add_argument("--headless", action="store_true")

    args = parser.parse_args()

    urls = []

    if args.url:
        urls.append(args.url)

    if args.file:
        urls.extend(load_urls_from_file(args.file))

    if not urls:
        print("Provide --url or --file")
        return

    # 🔥 Create ONE browser session
    driver = get_session(headless=args.headless)

    for url in urls:
        try:
            process_url(url, driver)
        except Exception as e:
            print("❌ Failed:", url, "|", e)


if __name__ == "__main__":
    main()