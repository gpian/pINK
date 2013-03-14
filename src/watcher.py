#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import os
import subprocess
import sys
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

logging.basicConfig(level=logging.ERROR)

src_path = os.getcwd()
root_path = os.path.dirname(src_path)
prints_path = '/'.join([root_path, 'prints'])
downloads_path = '/'.join([root_path, 'downloads'])
templates_path = '/'.join([root_path, 'templates'])

class WatcherEventHandler(FileSystemEventHandler):
    def __init__(self, template_filename, media_size):
        self.template_filename = template_filename
        self.media_size = media_size

    def on_created(self, event):
        print event.src_path
        image_path = event.src_path

        template_file = '/'.join([templates_path, self.template_filename])
        filename = os.path.basename(image_path)
        output_file = '/'.join([prints_path, filename])

        convert_parts = ['convert', '-size', '1200x1800', '-composite', template_file, image_path, '-geometry', '1180x1180+10+300', '-depth', '8', output_file]
        print convert_parts
        #subprocess.call(convert_parts)

        lpr_parts = ['lpr', '-o', 'media=%s' % self.media_size, output_file]
        print lpr_parts
        #subprocess.call(lpr_parts)

def main(args):
    media_sizes = ['A4', 'Letter', 'Legal', 'Custom.4x6in', 'Custom.2x3in']

    parser = argparse.ArgumentParser()
    parser.add_argument('--template', default='template.jpg', help='template filename (default template.jpg)')
    parser.add_argument('--size', default='Custom.4x6in', choices=media_sizes, help='size of paper (default 4x6in)')
    args = parser.parse_args()

    observer = Observer()
    event_handler = WatcherEventHandler(args.template, args.size)

    observer.schedule(event_handler, downloads_path, recursive=False)
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