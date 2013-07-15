#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import datetime as dt
import sys
import threading
import time

class Ingress(object):
    def __init__(self, rate):
        self.rate = rate
        self.is_running = False

    def start(self):
        if self.is_running == False:
            self.started_time = dt.datetime.utcnow()
            self.__start()
            self.is_running = True

    def __start(self):
        self.grab()
        self.__timer = threading.Timer(self.rate, self.__start)
        self.__timer.start()


    def stop(self):
        if self.is_running == True:
            self.__timer.cancel()
            self.__timer.join()
            self.is_running = False

    def grab(self):
        return 0

def main(argv):
    innlet = Ingress(30)
    innlet.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        innlet.stop()

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))