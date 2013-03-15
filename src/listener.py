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
from pINK import Paths

counter = 0
timer = None

paths = Paths(os.getcwd())

def grab_media(api, tag):
    global counter

    generator = api.tag_recent_media(10, '0', tag, as_generator=True)
    for page, next_url in generator:
        for media in page:
            counter = counter + 1
            url = media.get_standard_resolution_url()
            print "[%d] %s" % (counter, url)

            filename = ''.join([paths.downloads, '/', url.split('/')[-1]])
            r = requests.get(url)
            if not os.path.isfile(filename):
                with open(filename, "wb") as image:
                    image.write(r.content)

            url = media.user.profile_picture
            filename = ''.join([paths.pictures, '/', url.split('/')[-1]])
            r = requests.get(url)
            if not os.path.isfile(filename):
                with open(filename, "wb") as image:
                    image.write(r.content)


    global timer
    timer = threading.Timer(30, grab_media, [api, tag])
    timer.start()

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('hashtag', help='Instagram hashtag')
    args = parser.parse_args()

    unauthenticated_api = client.InstagramAPI(**CONFIG)
    grab_media(unauthenticated_api, args.hashtag)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        if timer is not None:
            timer.cancel()
    if timer is not None:
        timer.join()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))