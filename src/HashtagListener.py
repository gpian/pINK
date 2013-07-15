#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import requests
import sys
import time

from instagram import client, subscriptions
from Listener import Listener
from pINK import Paths
from SECRET import CONFIG

class HashtagListener(Listener):
    def __init__(self, api, hashtag, rate):
        super(HashtagListener, self).__init__(rate)

        self.api = api
        self.hashtag = hashtag
        self.counter = 0
        self.paths = Paths(os.getcwd())
        self.last_media_id = '0'

    def grab(self):
        print "API: tags/%s/media/recent?max_id=%s" % (self.hashtag, self.last_media_id)
        generator = self.api.tag_recent_media(10, self.last_media_id, self.hashtag, as_generator=True)
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

                try:
                    if self.last_media_ts < media.created_time:
                        self.last_media_ts = media.created_time
                        self.last_media_id = media.id
                        print "[last]", self.last_media_ts, self.last_media_id
                except AttributeError:
                    self.last_media_ts = media.created_time
                    self.last_media_id = media.id
                    print "[last]", self.last_media_ts, self.last_media_id

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('hashtag', help='Instagram hashtag')
    args = parser.parse_args()

    listener = HashtagListener(client.InstagramAPI(**CONFIG), args.hashtag, 30)
    listener.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        listener.stop()

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))