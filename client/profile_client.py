import json
from config import APP_ID
import requests

class ProfileClient:

    URL = "https://www.instagram.com/graphql/query"

    def _post(self, session, csrftoken, lsd, doc_id, friendly_name, variables):

        headers = {
            "x-ig-app-id": APP_ID,
            "x-csrftoken": csrftoken,
            "x-fb-lsd": lsd,
            "x-fb-friendly-name": friendly_name,
            "content-type": "application/x-www-form-urlencoded"
        }

        payload = {
            "fb_api_req_friendly_name": friendly_name,
            "doc_id": doc_id,
            "variables": json.dumps(variables)
        }

        r = session.post(self.URL, headers=headers, data=payload)

        print("GraphQL STATUS:", r.status_code)

        try:
            return r.json()
        except Exception:
            print("GraphQL returned non JSON")
            return None


    # -------- MAIN PIPELINE --------
    def fetch_full_profile(self, session, csrftoken, lsd, username, user_id):

        profile = {}

        # 1️⃣ PROFILE CORE INFO
        core = self._post(
            session, csrftoken, lsd,
            doc_id="26039052785710840",
            friendly_name="PolarisProfilePageContentQuery",
            variables={
                "id": user_id,
                "render_surface": "PROFILE"
            }
        )

        if core:
            profile["core"] = core

        # 2️⃣ HOVER CARD (BIO / CATEGORY)
        hover = self._post(
            session, csrftoken, lsd,
            doc_id="31530620256583767",
            friendly_name="PolarisUserHoverCardContentV2Query",
            variables={
                "userID": user_id,
                "username": username
            }
        )

        if hover:
            profile["hover"] = hover

        # 3️⃣ POSTS LIST
        posts = self._post(
            session, csrftoken, lsd,
            doc_id="24917539027921848",
            friendly_name="PolarisProfilePostsQuery",
            variables={
                "username": username,
                "data": {"count": 12}
            }
        )

        if posts:
            profile["posts"] = posts

        return profile
