#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import time

from pINK import Paths
from Egress import Egress

paths = Paths(os.getcwd())

class LprEgress(Egress):
    def __init__(self, watch_dir, template_filename, media_size):
        print "LprEgress on %s with %s at %s" % (watch_dir, template_filename, media_size)

        super(LprEgress, self).__init__(watch_dir)

        self.template_filename = template_filename
        self.media_size = media_size

    def process(self, watched_file):
        print "[%d] %s" % (self.counter, watched_file)

        image_file = watched_file
        print "Lpr process %s" % (image_file)

        template_file = '/'.join([paths.templates, self.template_filename])
        filename = os.path.basename(image_file)
        output_file = '/'.join([paths.prints, filename])

        convert_parts = ['convert', '-size', '1200x1800', '-composite', template_file, image_file, '-geometry', '1180x1180+10+300', '-depth', '8', output_file]
        subprocess.call(convert_parts)

        lpr_parts = ['lpr', '-o', 'media=%s' % self.media_size, output_file]
        subprocess.call(lpr_parts)

def main(args):
    media_sizes = ['A4', 'Letter', 'Legal', 'Custom.4x6in', 'Custom.2x3in']

    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', default=paths.downloads, help='directory to watch')
    parser.add_argument('--size', default='Custom.4x6in', choices=media_sizes, help='size of paper (default 4x6in)')
    parser.add_argument('--template', default='template.jpg', help='template filename (default template.jpg)')
    args = parser.parse_args()

    outlet = LprEgress(args.dir, args.template, args.size)
    outlet.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        outlet.stop()

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))