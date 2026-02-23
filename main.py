from unittest import result
from urllib.parse import urlparse
from client.token_extractor import TokenExtractor
from client.graphql_client import GraphQLClient
from behavior.human_behavior import HumanBehavior
from parsers.post_parser import PostParser
from cli import parse_args
from identity_pool.identity_manager import IdentityManager
from identity_pool.schedule_manager import ScheduleManager
from datetime import datetime
from client.profile_client import ProfileClient
from parsers.profile_parser import ProfileParser
from identity_pool.failover_executor import FailoverExecutor
from storage.snapshot_writer import store_snapshot
import time
import json
import os
import re


# ---------------- URL HELPERS ----------------

def detect_url_type(url):
    path = urlparse(url).path.strip("/").split("/")

    if not path or path[0] == "":
        return "unknown"

    if path[0] in ["p", "reel"]:
        return "post"

    return "profile"


def get_shortcode(url):
    return urlparse(url).path.strip("/").split("/")[-1]


def get_username(url):
    return urlparse(url).path.strip("/").split("/")[0]


# ---------------- SCRAPER ----------------

def scrape_any(identity, url):

    session = identity.session
    url_type = detect_url_type(url)

    print(f"\n[Identity: {identity.name}] Visiting {url_type.upper()} {url}")

    # behave like human
    HumanBehavior(session, identity.name).warmup()

    # open page
    r = session.get(url)
    print("BOOTSTRAP STATUS:", r.status_code)

    csrftoken, lsd = TokenExtractor.extract(r.text, session)

    # ================== POST ==================
    if url_type == "post":

        shortcode = get_shortcode(url)

        data = GraphQLClient().fetch_post(session, csrftoken, lsd, shortcode)
        result = PostParser.extract(data, shortcode)

        if result:
            result["type"] = "post"
            result["url"] = url

            print(
                f"✔ Extracted: {result['username']} | "
                f"{result['likes']} likes | "
                f"{result['comments']} comments"
            )

        return result

    # ================== PROFILE ==================
    if url_type == "profile":

        username = get_username(url)

        # STEP 1: extract numeric user id
        user_id = TokenExtractor.extract_user_id(r.text)

        # STEP 2: fetch graphql profile endpoints
        profile_data = ProfileClient().fetch_full_profile(
            session=session,
            csrftoken=csrftoken,
            lsd=lsd,
            username=username,
            user_id=user_id
        )

        # STEP 3: try graphql parser
        result = ProfileParser.extract(profile_data)

        if result:
            result["type"] = "profile"
            result["url"] = f"https://www.instagram.com/{result['username']}/"

            print(
                f"✔ Profile: {result['username']} | "
                f"{result['followers']} followers | "
                f"{result['posts']} posts"
            )
            return result

        # ---------- FALLBACK 1 : JSON inside HTML ----------
        print("Falling back to HTML profile parse...")
        profile = ProfileParser.extract_from_html(r.text, username)

        if profile:
            profile["type"] = "profile"
            profile["url"] = url
            print(
                f"✔ Profile (JSON): {profile['username']} | "
                f"{profile['followers']} followers | "
                f"{profile['posts']} posts"
            )
            return profile

        # ---------- FALLBACK 2 : META TAG ----------
        match = re.search(
            r'content="([^"]+?) Followers, ([^"]+?) Following, ([^"]+?) Posts',
            r.text
        )

        if match:
            profile = {
                "type": "profile",
                "username": username,
                "url": url,
                "followers": match.group(1),
                "following": match.group(2),
                "posts": match.group(3),
                "source": "html_meta_fallback"
            }

            print(f"⚠ Meta fallback used: {username}")
            return profile

        raise Exception("Profile parsing failed completely")

    return None


# ---------------- STORAGE ----------------

def save_snapshot(item):

    if not item:
        return

    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")

    if item["type"] == "profile":
        folder = f"data/profiles/{item['username']}"
    elif item["type"] == "post":
        folder = f"data/posts/{item['shortcode']}"
    else:
        folder = "data/unknown"

    os.makedirs(folder, exist_ok=True)

    path = os.path.join(folder, f"{timestamp}.json")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(item, f, indent=2, ensure_ascii=False)

    print(f"💾 Stored snapshot → {path}")


# ---------------- PROCESSOR ----------------
def process_url(identity_manager, url, results):

    executor = FailoverExecutor(identity_manager)

    def job(identity, url):
        return scrape_any(identity, url)

    try:
        result = executor.run(job, url)

        if result:
            results.append(result)
            store_snapshot(result)

    except Exception as e:
        print("❌ FINAL FAILURE:", url, "|", e)


# ---------------- ENTRY ----------------

def main():

    args = parse_args()
    identity_manager = IdentityManager()

    if args.url:
        process_url(identity_manager, args.url, results)

    elif args.file:
        results = []
        with open(args.file) as f:
            for line in f:
                url = line.strip()
                if url:
                    process_url(identity_manager, url, results)

    else:
        print("Provide URL or --file")
        return

    print("\nDone. Snapshots saved to data/ folder")


if __name__ == "__main__":
    main()