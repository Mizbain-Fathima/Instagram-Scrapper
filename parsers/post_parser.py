class PostParser:

    @staticmethod
    def _get_like_count(media):
        return media.get("edge_media_preview_like", {}).get("count", 0)

    @staticmethod
    def _get_comment_count(media):
        # Instagram changes this field name depending on media type
        if "edge_media_to_comment" in media:
            return media["edge_media_to_comment"].get("count", 0)

        if "edge_media_to_parent_comment" in media:
            return media["edge_media_to_parent_comment"].get("count", 0)

        return 0

    @staticmethod
    def _get_caption(media):
        edges = media.get("edge_media_to_caption", {}).get("edges", [])
        if edges:
            return edges[0]["node"].get("text", "")
        return ""

    @staticmethod
    def _get_media_type(media):
        typename = media.get("__typename", "")

        if typename == "XDTGraphVideo":
            return "video"
        if typename == "XDTGraphSidecar":
            return "carousel"
        return "image"

    @staticmethod
    def _get_media_url(media):
        return media.get("display_url") or media.get("thumbnail_src")

    @staticmethod
    def extract(data, shortcode):

        media = data.get("data", {}).get("xdt_shortcode_media")
        if not media:
            return None

        return {
            "shortcode": shortcode,
            "username": media.get("owner", {}).get("username"),
            "likes": PostParser._get_like_count(media),
            "comments": PostParser._get_comment_count(media),
            "caption": PostParser._get_caption(media),
            "media_type": PostParser._get_media_type(media),
            "media_url": PostParser._get_media_url(media)
        }
