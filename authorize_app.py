import argparse
import json

from auth import session_from_keys


def main():
    parser = argparse.ArgumentParser(description="Authorizes the app specified via the keyfile for a Tumbler account")
    parser.add_argument("--keyfile", required=True, help="The JSON file which contains the Tumblr OAuth app key and secret key")
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

    session_from_keys(key=api_key, secret_key=api_secret_key)
