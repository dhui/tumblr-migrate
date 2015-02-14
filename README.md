tumblr-migrate
==============

Tools to migrate posts from one Tumblr blog to another Tumbler blog


Setup
=====

1. Create a Tumblr app if you don't already have one
1. Put your Tumblr OAuth key and secret key in a keyfile. With the following format:

    ```{"key": "KEY", "secret_key": "SECRET_KEY"}```

1. Make sure both blogs have authorized your app. You can do this by logging into Tumblr in your web browser, run `authorize_app.py`, and follow the instructions.



Usage
=====

To copy posts between blogs use: `copy_posts.py`

To update posts on one blog using the posts from another, use: `update_posts.py`

To wipe a blog clean, use: `delete_all_posts.py`


Notes
=====

* Not using [pytumblr](https://github.com/tumblr/pytumblr) because as of 12/9/2014, the API for posting blog posts is split based on post type.
    * There's an internal API called `_send_post()` which takes the the post type as an argument. `_send_post()` validates the params and doesn't allow extraneous params to be sent.


TODO
====
* Package the repo so it's pip installable
