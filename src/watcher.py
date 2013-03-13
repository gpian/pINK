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

class WatcherEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        print event.src_path

        cwd = os.getcwd()
        project_root = os.path.dirname(cwd)
        prints_path = '/'.join([project_root, 'prints'])
        template_file = '/'.join([cwd, 'template.jpg'])
        filename = os.path.basename(event.src_path)
        output_file = '/'.join([prints_path, filename])

        convert_parts = ['convert', '-size', '1200x1800', '-composite', template_file, event.src_path, '-geometry', '1180x1180+10+300', '-depth', '8', output_file]
        subprocess.call(convert_parts)

        lpr_parts = ['lpr', '-o', 'media=Custom.4x6in', output_file]
        subprocess.call(lpr_parts)

def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', help='Directory to watch')
    args = parser.parse_args()

    observer = Observer()
    event_handler = WatcherEventHandler()

    observer.schedule(event_handler, args.directory, recursive=False)
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