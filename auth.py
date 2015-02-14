import json

import requests_oauthlib

from constants import CALLBACK_URL, REQUEST_TOKEN_URL, AUTHORIZATION_BASE_URL, ACCESS_TOKEN_URL, USER_INFO_URL


def session_from_keys(key, secret_key, session_filename=None):
    """
    Gets an OAuth1 Authenticated session with the given keys.
    Will prompt the user to visit urls and input the redirected url.
    """
    session = requests_oauthlib.OAuth1Session(client_key=key, client_secret=secret_key, callback_uri=CALLBACK_URL)
    session.fetch_request_token(REQUEST_TOKEN_URL)
    url = session.authorization_url(AUTHORIZATION_BASE_URL)
    print "Authorize the app at this URL: %s" % url
    redirect_response = raw_input("Paste full redirect URL: ")
    session.parse_authorization_response(redirect_response)
    session.fetch_access_token(ACCESS_TOKEN_URL)

    if session_filename:
        session_data = {
            "client_key": session.auth.client.client_key,
            "client_secret": session.auth.client.client_secret,
            "resource_owner_key": session.auth.client.resource_owner_key,
            "resource_owner_secret": session.auth.client.resource_owner_secret,
        }

        with open(session_filename, "w") as session_file:
            json.dump(session_data, session_file)

    return session


def load_session(session_filename, key, secret_key):
    session_data = {}
    try:
        with open(session_filename) as session_file:
            session_data = json.load(session_file)
    except IOError:
        pass

    session_data_client_key = session_data.get("client_key")
    session_data_client_secret = session_data.get("client_secret")
    session_data_resource_owner_key = session_data.get("resource_owner_key")
    session_data_resource_owner_secret = session_data.get("resource_owner_secret")

    if session_data_client_key and session_data_client_secret and \
       session_data_resource_owner_key and session_data_resource_owner_secret and \
       session_data_client_key == key and session_data_client_secret == secret_key:

        # Validate session
        session = requests_oauthlib.OAuth1Session(client_key=session_data_client_key,
                                                  client_secret=session_data_client_secret,
                                                  resource_owner_key=session_data_resource_owner_key,
                                                  resource_owner_secret=session_data_resource_owner_secret)
        response = session.get(USER_INFO_URL)
        if response.status_code != 200:
            print "Saved session is invalid"
            session = session_from_keys(session_filename=session_filename, key=key, secret_key=secret_key)
    else:
        print "Couldn't load saved session"
        session = session_from_keys(session_filename=session_filename, key=key, secret_key=secret_key)

    return session
