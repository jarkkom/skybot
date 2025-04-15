from __future__ import unicode_literals

import re
from urllib.parse import quote
from util import hook, http


def get_bsky_post(profile, rkey):
    # resolve profile to DID
    try:
        did_json = http.get_json('https://public.api.bsky.app/xrpc/com.atproto.identity.resolveHandle',
                                    query_params={'handle': profile})
        did = did_json['did']
    except http.HTTPError as e:
        return "error: unknown %s" % e.code

    # construct AT URI
    uri = f'at://{did}/app.bsky.feed.post/{rkey}'

    # Fetch the post thread using the public API
    try:
        post_json = http.get_json('https://public.api.bsky.app/xrpc/app.bsky.feed.getPostThread', query_params={'uri': uri})
    except http.HTTPError as e:
        return "error: unknown %s" % e.code

    try:
        post_content = post_json['thread']['post']['record']['text']
    except KeyError:
        return None

    try:
        posted_at = post_json['thread']['post']['record']['createdAt']
    except KeyError:
        posted_at = ""

    images = ""
    try:
        imgs = []
        for i in post_json['thread']['post']['embed']['images']:
            imgs.append(i['fullsize'])

        images = " ".join(imgs)
    except KeyError:
        images = ""

    return f"{posted_at} {post_content} {images}"


@hook.regex(r"https?://bsky.app/profile/([_0-9a-zA-Z\.]+)/post/([a-z0-9]+)")
def show_bsky(match):
    return get_bsky_post(match.group(1), match.group(2))

