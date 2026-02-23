# cli.py

import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Instagram Scraper")

    parser.add_argument(
        "url",
        nargs="?",
        help="Single Instagram post URL"
    )

    parser.add_argument(
        "--file",
        help="File containing URLs (one per line)"
    )

    return parser.parse_args()
