#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import subprocess
import sys
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

logging.basicConfig(level=logging.ERROR)

class WatcherEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        print event.src_path
        subprocess.call(['lpr', '-P', 'CUPS_PDF', event.src_path])

def main():
    observer = Observer()
    event_handler = WatcherEventHandler()

    observer.schedule(event_handler, sys.argv[1], recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    return 0

if __name__ == "__main__":
    sys.exit(main())