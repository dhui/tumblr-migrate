GET_POSTS_URL_BASE = "https://api.tumblr.com/v2/blog/%(blog_name)s.tumblr.com/posts/"  # Auths via key
CREATE_POST_URL_BASE = "https://api.tumblr.com/v2/blog/%(blog_name)s.tumblr.com/post/"  # Auths via OAuth
USER_INFO_URL = "https://api.tumblr.com/v2/user/info/"  # Auths via OAuth

POST_LIMIT = 20  # 20 is the max Tumblr supports

POST_ATTRS_TO_FILTER = ("id", "reblog_key", "blog_name", "post_url", "short_url", "liked", "followed", "highlighted", "can_reply", "note_count")
EDIT_POST_ATTRS_TO_FILTER = ("reblog_key", "blog_name", "post_url", "short_url", "liked", "followed", "highlighted", "can_reply", "note_count")

SUPPORTED_POST_IMPORT_TYPES = ("text",)


CALLBACK_URL = "https://www.tumblr.com/dashboard"
REQUEST_TOKEN_URL = "https://www.tumblr.com/oauth/request_token"
AUTHORIZATION_BASE_URL = "https://www.tumblr.com/oauth/authorize"
ACCESS_TOKEN_URL = "https://www.tumblr.com/oauth/access_token"

DEFAULT_SESSION_FILE = "session.json"
