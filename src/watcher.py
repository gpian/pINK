#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import os
import subprocess
import sys
import time
import threading

from pINK import Paths
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

logging.basicConfig(level=logging.ERROR)

paths = Paths(os.getcwd())

class WatcherEventHandler(FileSystemEventHandler):
    def __init__(self, template_filename, media_size):
        self.template_filename = template_filename
        self.media_size = media_size
        self.counter = 0

    def on_created(self, event):
        self.counter = self.counter + 1
        print "[%d] %s" % (self.counter, event.src_path)

        threading.Thread(target=self.process, args=(event.src_path,)).start()

    def process(self, image_file):
        template_file = '/'.join([paths.templates, self.template_filename])
        filename = os.path.basename(image_file)
        output_file = '/'.join([paths.prints, filename])

        convert_parts = ['convert', '-size', '1200x1800', '-composite', template_file, image_file, '-geometry', '1180x1180+10+300', '-depth', '8', output_file]
        subprocess.call(convert_parts)

        lpr_parts = ['lpr', '-o', 'media=%s' % self.media_size, output_file]
        subprocess.call(lpr_parts)

        mv_parts = ['mv', image_file, paths.originals]
        subprocess.call(mv_parts)

def main(args):
    media_sizes = ['A4', 'Letter', 'Legal', 'Custom.4x6in', 'Custom.2x3in']

    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', default=paths.downloads, help='directory to watch')
    parser.add_argument('--size', default='Custom.4x6in', choices=media_sizes, help='size of paper (default 4x6in)')
    parser.add_argument('--template', default='template.jpg', help='template filename (default template.jpg)')
    args = parser.parse_args()

    observer = Observer()
    event_handler = WatcherEventHandler(args.template, args.size)
    observer.schedule(event_handler, args.dir, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))