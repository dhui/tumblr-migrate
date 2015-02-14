import argparse
import json

from auth import load_session
from constants import GET_POSTS_URL_BASE, CREATE_POST_URL_BASE, POST_LIMIT, DEFAULT_SESSION_FILE

DELETE_POST_BASE_URL = CREATE_POST_URL_BASE + "delete/"  # urlparse and urllib are crap. Just concatenate for simplicity.


def get_post_ids(session, api_key, blog_name):
    post_ids = set()
    url = GET_POSTS_URL_BASE % {"blog_name": blog_name}
    offset = 0

    params = {
        "offset": offset,
        "limit": POST_LIMIT,
        "api_key": api_key  # Tumblr's API is inconsistent about it's authn mechanisms
    }

    posts_remaining = 1
    status_ok = True

    while status_ok and posts_remaining > 0:
        response = session.get(url, params=params)

        # parse response
        response_json = response.json()
        total_posts = response_json.get("response", {}).get("total_posts", 0)
        post_ids.update(p.get("id") for p in response_json.get("response", {}).get("posts", []))

        # Update params for next request
        offset += POST_LIMIT
        params["offset"] = offset

        # Update exit conditions
        status_ok = response.status_code == 200 and response_json.get("meta", {}).get("status", 400) == 200
        posts_remaining = total_posts - len(post_ids)

    return post_ids


def delete_posts(session, api_key, blog_name):
    post_ids = get_post_ids(session=session, api_key=api_key, blog_name=blog_name)
    url = DELETE_POST_BASE_URL % {"blog_name": blog_name}
    for post_id in post_ids:
        response = session.post(url, data={"id": post_id})
        if response.status_code != 200:
            print "Couldn't delete post: %s" % post_id


def main():
    parser = argparse.ArgumentParser(description="Deletes all of the posts for the given Tumblr account")
    parser.add_argument("--keyfile", required=True, help="The JSON file which contains the Tumblr OAuth app key and secret key")
    parser.add_argument("--blog", required=True, help="The name of the blog delete posts for")
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

    print "About to delete all posts for: %s" % options.blog
    response = raw_input("Are you sure you want to continue? [y/n]")
    if response[0].lower() != "y":
        print "Exiting..."
        return

    session = load_session(session_filename=options.session, key=api_key, secret_key=api_secret_key)

    delete_posts(session=session, api_key=api_key, blog_name=options.blog)


if __name__ == "__main__":
    main()
