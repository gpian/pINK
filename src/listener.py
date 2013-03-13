#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bottle
from bottle import route, post, run, request
from instagram import client, subscriptions
import requests
import os, sys
import time, threading

bottle.debug(True)

TAG = "photobox"
DOWNLOAD_DIR = "../downloads"
CONFIG = {
    'client_id': 'ce3ac3be70ee4089bc7317b2959a043c',
    'client_secret': '8c17ab619c624ed0aa5e1c5dd691cb2a',
    'redirect_uri': 'http://localhost:8515/oauth_callback'
}

api = None
unauthenticated_api = client.InstagramAPI(**CONFIG)

@route('/')
def home():
    try:
        url = unauthenticated_api.get_authorize_url(scope=["likes","comments"])
        return '<a href="%s">Connect with Instagram</a>' % url
    except Exception, e:
        print e

@route('/oauth_callback')
def on_callback():
    global api
    code = request.GET.get("code")
    if not code:
        return 'Missing code'
    try:
        access_token, user_info = unauthenticated_api.exchange_code_for_access_token(code)
        if not access_token:
            return 'Could not get access token'
        
        api = client.InstagramAPI(access_token=access_token)
        grab_media()

        return 'Done'
    except Exception, e:
        print e

def grab_media():
    global DOWNLOAD_DIR, TAG, T

    recent_media, next = api.tag_recent_media(10, '0', TAG)
    for media in recent_media:
        url = media.images['standard_resolution'].url
        filename = ''.join([DOWNLOAD_DIR, '/', url.split('/')[-1]])
        r = requests.get(url)
        if not os.path.isfile(filename):
            with open(filename, "wb") as image:
                image.write(r.content)
    threading.Timer(30, grab_media).start()

def main():
    global TAG
    TAG = sys.argv[1]
    run(host='localhost', port=8515, reloader=True)

if __name__ == '__main__':
    main()