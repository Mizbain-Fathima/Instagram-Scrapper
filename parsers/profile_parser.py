import re
import json

class ProfileParser:

    # -------- GRAPHQL PARSER --------
    @staticmethod
    def extract(data):

        if not data or "core" not in data:
            return None

        try:
            user = data["core"]["data"]["user"]

            result = {
                "username": user.get("username"),
                "followers": user.get("edge_followed_by", {}).get("count"),
                "following": user.get("edge_follow", {}).get("count"),
                "posts": user.get("edge_owner_to_timeline_media", {}).get("count"),
                "is_private": user.get("is_private"),
                "is_verified": user.get("is_verified"),
                "source": "graphql"
            }

            # optional hover data (may fail with 401)
            if "hover" in data and data["hover"]:
                hover_user = data["hover"].get("data", {}).get("user", {})
                result["biography"] = hover_user.get("biography")
                result["category"] = hover_user.get("category_name")

            return result

        except Exception:
            return None


    @staticmethod
    def extract_from_html(html, username):

        # Find hydration JSON
        match = re.search(
            r'window\.__additionalDataLoaded\([^,]+,\s*(\{.*?\})\);',
            html
        )

        if not match:
            return None

        try:
            data = json.loads(match.group(1))

            user = data.get("graphql", {}).get("user", {})
            if not user:
                return None

            return {
                "username": user.get("username"),
                "followers": user.get("edge_followed_by", {}).get("count"),
                "following": user.get("edge_follow", {}).get("count"),
                "posts": user.get("edge_owner_to_timeline_media", {}).get("count"),
                "biography": user.get("biography"),
                "is_private": user.get("is_private"),
                "is_verified": user.get("is_verified"),
                "category": user.get("category_name"),
                "external_url": user.get("external_url"),
                "profile_pic": user.get("profile_pic_url_hd"),
                "source": "html_hydration"
            }

        except Exception:
            return None