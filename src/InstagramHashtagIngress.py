#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import requests
import sys
import time

from instagram import client, subscriptions
from Ingress import Ingress
from pINK import Paths
from SECRET import CONFIG

class InstagramHashtagIngress(Ingress):
    def __init__(self, api, hashtag, rate):
        super(InstagramHashtagIngress, self).__init__(rate)

        self.api = api
        self.hashtag = hashtag
        self.counter = 0
        self.paths = Paths(os.getcwd())
        self.last_media_id = '0'
        self.last_media_ts = None

    def grab(self):
        generator = self.api.tag_recent_media(10, self.last_media_id, self.hashtag, as_generator=True)
        for page, next_url in generator:
            for media in page:

                url = media.get_standard_resolution_url()
                filename = '/'.join([self.paths.downloads, url.split('/')[-1]])

                if media.created_time > self.started_time:
                    self.counter = self.counter + 1

                    r = requests.get(url)
                    if not os.path.isfile(filename):
                        with open(filename, "wb") as image:
                            image.write(r.content)

                            if self.last_media_ts == None or self.last_media_ts < media.created_time:
                                self.last_media_ts = media.created_time
                                self.last_media_id = media.id
                                print "[*] %s %s %s" % (media.created_time, filename, media.id)
                            else:
                                print "[+] %s %s %s" % (media.created_time, filename, media.id)

                    url = media.user.profile_picture
                    filename = ''.join([self.paths.pictures, '/', url.split('/')[-1]])
                    r = requests.get(url)
                    if not os.path.isfile(filename):
                        with open(filename, "wb") as image:
                            image.write(r.content)

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('hashtag', help='Instagram hashtag')
    args = parser.parse_args()

    innlet = InstagramHashtagIngress(client.InstagramAPI(**CONFIG), args.hashtag, 30)
    innlet.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        innlet.stop()

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))