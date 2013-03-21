#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import datetime as dt
import os
import requests
import sys
import time
import threading

from instagram import client, subscriptions
from SECRET import CONFIG
from pINK import Paths

class Listener:
    def __init__(self, api, hashtag):
        self.api = api
        self.hashtag = hashtag
        self.counter = 0
        self.paths = Paths(os.getcwd())
        self.last_media_id = '0'

    def start(self):
        self.started_time = dt.datetime.utcnow()
        self.grab_media()

    def stop(self):
        self.timer.cancel()
        self.timer.join()

    def grab_media(self):
        generator = self.api.tag_recent_media(10, self.last_media_id, self.hashtag, as_generator=True)
        #generator = self.api.tag_recent_media(10, '0', self.hashtag, as_generator=True)
        for page, next_url in generator:
            for media in page:

                url = media.get_standard_resolution_url()
                filename = '/'.join([self.paths.downloads, url.split('/')[-1]])

                if media.created_time > self.started_time:
                    self.counter = self.counter + 1

                    print "[+] %s %s" % (media.created_time, media.id)

                    r = requests.get(url)
                    if not os.path.isfile(filename):
                        with open(filename, "wb") as image:
                            image.write(r.content)

                    url = media.user.profile_picture
                    filename = ''.join([self.paths.pictures, '/', url.split('/')[-1]])
                    r = requests.get(url)
                    if not os.path.isfile(filename):
                        with open(filename, "wb") as image:
                            image.write(r.content)
                else:
                    print "[-] %s %s" % (media.created_time, media.id)

                try:
                    if self.last_media_ts < media.created_time:
                        self.last_media_ts = media.created_time
                        self.last_media_id = media.id
                        print "[last]", self.last_media_id, self.last_media_ts
                except AttributeError:
                    self.last_media_ts = media.created_time
                    self.last_media_id = media.id
                    print "[last]", self.last_media_id, self.last_media_ts

        self.timer = threading.Timer(30, self.grab_media)
        self.timer.start()

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('hashtag', help='Instagram hashtag')
    args = parser.parse_args()

    listener = Listener(client.InstagramAPI(**CONFIG), args.hashtag)
    listener.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        listener.stop()

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))