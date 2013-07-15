#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import os
import sys
import threading
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

logging.basicConfig(level=logging.ERROR)

class Egress(FileSystemEventHandler):
    def __init__(self, watch_dir):
        self.watch_dir = watch_dir

        self.counter = 0
        self.observer = Observer()
        self.is_started = False;

    def start(self):
        if self.is_started == False:
            self.observer.schedule(self, self.watch_dir, recursive=False)
            self.observer.start()
            self.is_started = True

    def stop(self):
        if self.is_started == True:
            self.observer.stop()
            self.observer.join()
            self.is_started = False

    def on_created(self, event):
        self.counter = self.counter + 1
        threading.Thread(target=self.process, args=(event.src_path,)).start()

    def process(self, watched_file):
        print "[%d] %s" % (self.counter, watched_file)
        return 0

def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', default='.', help='directory to watch')
    args = parser.parse_args()

    outlet = Egress(args.dir)
    outlet.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        outlet.stop()

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))