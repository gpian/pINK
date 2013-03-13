#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import requests
import os
import sys
import time
import threading

from instagram import client, subscriptions

CONFIG = {
    'client_id': 'ce3ac3be70ee4089bc7317b2959a043c',
    'client_secret': '8c17ab619c624ed0aa5e1c5dd691cb2a',
    'redirect_uri': 'http://localhost:8515/oauth_callback'
}

def grab_media(api, tag, download_dir):
    recent_media, next = api.tag_recent_media(10, '0', tag)
    for media in recent_media:
        url = media.images['standard_resolution'].url
        print url

        filename = ''.join([download_dir, '/', url.split('/')[-1]])
        r = requests.get(url)
        if not os.path.isfile(filename):
            with open(filename, "wb") as image:
                image.write(r.content)
    threading.Timer(30, grab_media, [api, tag, download_dir]).start()

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('hashtag', help='Instagram hashtag')
    parser.add_argument('directory', help='Output directory')
    args = parser.parse_args()

    unauthenticated_api = client.InstagramAPI(**CONFIG)
    grab_media(unauthenticated_api, args.hashtag, args.directory)

if __name__ == '__main__':
    sys.exit(main(sys.argv))