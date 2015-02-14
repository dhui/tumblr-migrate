import argparse
import collections
import copy
import json

from auth import load_session
from constants import GET_POSTS_URL_BASE, CREATE_POST_URL_BASE, POST_LIMIT, EDIT_POST_ATTRS_TO_FILTER, SUPPORTED_POST_IMPORT_TYPES, DEFAULT_SESSION_FILE

EDIT_POST_BASE_URL = CREATE_POST_URL_BASE + "edit/"  # urlparse and urllib are crap. Just concatenate for simplicity.


def export_posts(session, api_key, blog_name, export_notes=False, export_reblogs=False):
    posts = {}
    url = GET_POSTS_URL_BASE % {"blog_name": blog_name}
    offset = 0

    params = {
        "offset": offset,
        "limit": POST_LIMIT,
        "api_key": api_key  # Tumblr's API is inconsistent about it's authn mechanisms
    }
    if export_notes:
        params["notes_info"] = "true"
    if export_reblogs:
        params["reblog_info"] = "true"

    posts_remaining = 1
    status_ok = True

    while status_ok and posts_remaining > 0:
        response = session.get(url, params=params)

        # parse response
        response_json = response.json()
        total_posts = response_json.get("response", {}).get("total_posts", 0)
        posts.update({p.get("id"): p for p in response_json.get("response", {}).get("posts", [])})

        # Update params for next request
        offset += POST_LIMIT
        params["offset"] = offset

        # Update exit conditions
        status_ok = response.status_code == 200 and response_json.get("meta", {}).get("status", 400) == 200
        posts_remaining = total_posts - len(posts)

    sorted_posts = sorted((p for p in posts.itervalues()), key=lambda x: x.get("timestamp"))
    print "Post type counts:"
    print collections.Counter(p.get("type") for p in posts.itervalues())
    return sorted_posts


def clean_post(post):
    """
    Given a Tumblr post, returns a clean version of the post
    """
    cleaned_post = copy.deepcopy(post)
    for attr in EDIT_POST_ATTRS_TO_FILTER:
        try:
            del cleaned_post[attr]
        except KeyError:
            pass

    # Tags are POSTed in a different format (string) than they're retrieved (list)
    if "tags" in cleaned_post:
        cleaned_post["tags"] = u",".join(post["tags"])
    return cleaned_post


def edit_posts(session, dest_blog_name, src_posts, dest_posts):
    # filter out attributes that can't be POSTed
    clean_src_posts = [clean_post(p) for p in src_posts if p.get("type") in SUPPORTED_POST_IMPORT_TYPES]

    slug_to_dest_post_id = {p.get("slug"): p.get("id") for p in dest_posts}

    url = EDIT_POST_BASE_URL % {"blog_name": dest_blog_name}

    for src_post in clean_src_posts:
        dest_post_id = slug_to_dest_post_id.get(src_post.get("slug"))

        if not dest_post_id:
            continue

        new_dest_post = copy.deepcopy(src_post)
        new_dest_post["id"] = dest_post_id
        response = session.post(url, data=new_dest_post)
        if response.status_code != 200:
            print "Failed to edit post..."
            print response
            print response.content
            print new_dest_post


def main():
    parser = argparse.ArgumentParser(description="Updates the posts in the dest Tumblr blog using the posts from the src. Assumes that posts in the src and dest blog have the same slug.")
    parser.add_argument("--keyfile", required=True, help="The JSON file which contains the Tumblr OAuth app key and secret key")
    parser.add_argument("--src", required=True, help="The name of the blog to get posts from")
    parser.add_argument("--dest", required=True, help="The name of the blog to update")
    parser.add_argument("--session", default=DEFAULT_SESSION_FILE, help="The file used to cache the session information")
    options = parser.parse_args()

    api_keys = {}
    with open(options.keyfile) as keyfile:
        api_keys = json.load(keyfile)

    if not api_keys:
        print "Error: No API keys found..."
        print "Exiting..."
        return

    api_key = api_keys.get("key")
    api_secret_key = api_keys.get("secret_key")

    if api_key is None:
        print "Error: API key not found in file: %s" % options.keyfile
        print "Exiting..."
        return

    if api_secret_key is None:
        print "Error: API secret key not found in file: %s" % options.keyfile
        print "Exiting..."
        return

    session = load_session(session_filename=options.session, key=api_key, secret_key=api_secret_key)

    src_posts = export_posts(session=session, api_key=api_key, blog_name=options.src)
    dest_posts = export_posts(session=session, api_key=api_key, blog_name=options.dest)
    edit_posts(session=session, dest_blog_name=options.dest, src_posts=src_posts, dest_posts=dest_posts)


if __name__ == "__main__":
    main()
