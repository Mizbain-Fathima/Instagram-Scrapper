import re

class TokenExtractor:

    @staticmethod
    def extract(html, session):

        if not html or len(html) < 5000:
            raise Exception("Instagram returned minimal page (blocked)")

        # only block true JS challenge
        if "Please enable JavaScript to continue" in html:
            raise Exception("Blocked by JS challenge")

        # extract tokens
        csrftoken = session.cookies.get("csrftoken")

        # new robust LSD extraction (pattern changes frequently)
        lsd_match = re.search(r'"LSD",\[\],{"token":"(.*?)"}', html)
        if not lsd_match:
            lsd_match = re.search(r'"lsd":"(.*?)"', html)

        lsd = lsd_match.group(1) if lsd_match else None

        if not csrftoken or not lsd:
            print("\n--- TOKEN DEBUG ---")
            print("csrftoken:", csrftoken)
            print("lsd:", lsd)
            print(html[:800])
            print("-------------------\n")

            raise Exception("Failed to extract tokens")

        return csrftoken, lsd


    @staticmethod
    def extract_user_id(html: str):
        """
        Extract numeric Instagram user id from profile bootstrap HTML
        """

        # Modern IG structure
        match = re.search(r'"profilePage_(\d+)"', html)
        if match:
            return match.group(1)

        # Backup structure
        match = re.search(r'"id":"(\d{5,})","username"', html)
        if match:
            return match.group(1)

        raise Exception("User ID not found in HTML (profile may not exist or blocked)")