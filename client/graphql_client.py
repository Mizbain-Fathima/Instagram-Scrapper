# graphql_client.py

import json
from config import DOC_ID, APP_ID, PROFILE_DOC_ID

class GraphQLClient:

    URL = "https://www.instagram.com/graphql/query"

    def fetch_post(self, session, csrftoken, lsd, shortcode):

        headers = {
            "x-ig-app-id": APP_ID,
            "x-csrftoken": csrftoken,
            "x-fb-lsd": lsd,
            "x-fb-friendly-name": "PolarisFeedTimelineRootV2Query",
            "content-type": "application/x-www-form-urlencoded"
        }

        payload = {
            "fb_api_req_friendly_name": "PolarisPostActionLoadPostQuery",
            "doc_id": DOC_ID,
            "variables": json.dumps({
                "shortcode": shortcode,
                "fetch_comment_count": 40,
                "fetch_related_profile_media_count": 0,
                "parent_comment_count": 24,
                "child_comment_count": 3,
                "fetch_like_count": 10,
                "fetch_tagged_user_count": None,
                "fetch_preview_comment_count": 2,
                "has_threaded_comments": True,
                "hoisted_comment_id": None,
                "hoisted_reply_id": None
            })
        }


        r = session.post(self.URL, headers=headers, data=payload)

        print("Status:", r.status_code)
        print("Content-Type:", r.headers.get("content-type"))

        try:
            data = r.json()
        except Exception:
            print("\n====== INSTAGRAM RESPONSE START ======")
            print(r.text[:700])
            print("====== INSTAGRAM RESPONSE END ======\n")
            raise Exception("Response is not JSON")

        return data

    def fetch_profile(self, session, csrftoken, lsd, user_id):
        """
        Fetch profile metadata using PolarisProfilePageContentQuery
        """

        headers = {
            "x-ig-app-id": APP_ID,
            "x-csrftoken": csrftoken,
            "x-fb-lsd": lsd,
            "x-fb-friendly-name": "PolarisProfilePageContentQuery",
            "content-type": "application/x-www-form-urlencoded"
        }

        payload = {
            "fb_api_req_friendly_name": "PolarisProfilePageContentQuery",
            "doc_id": PROFILE_DOC_ID,
            "variables": json.dumps({
                "id": user_id,
                "render_surface": "PROFILE"
            })
        }

        r = session.post(self.URL, headers=headers, data=payload)

        print("GraphQL STATUS:", r.status_code)

        try:
            data = r.json()
        except Exception:
            print(r.text[:500])
            raise Exception("Profile GraphQL returned non-JSON")

        return data
