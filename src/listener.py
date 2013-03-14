#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import requests
import os
import sys
import time
import threading

from instagram import client, subscriptions
from SECRET import CONFIG

src_path = os.getcwd()
root_path = os.path.dirname(src_path)
downloads_path = '/'.join([root_path, 'downloads'])

def grab_media(api, tag):
    recent_media, next = api.tag_recent_media(10, '0', tag)
    for media in recent_media:
        url = media.images['standard_resolution'].url
        print url

        filename = ''.join([downloads_path, '/', url.split('/')[-1]])
        r = requests.get(url)
        if not os.path.isfile(filename):
            with open(filename, "wb") as image:
                image.write(r.content)
    threading.Timer(30, grab_media, [api, tag]).start()

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('hashtag', help='Instagram hashtag')
    args = parser.parse_args()

    unauthenticated_api = client.InstagramAPI(**CONFIG)

    grab_media(unauthenticated_api, args.hashtag)

if __name__ == '__main__':
    sys.exit(main(sys.argv))