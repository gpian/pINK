#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

class Paths:
    def __init__(self, src):
        self.src        = src
        self.root       = os.path.dirname(self.src)
        self.downloads  = '/'.join([self.root, 'downloads'])
        self.originals  = '/'.join([self.root, 'originals'])
        self.prints     = '/'.join([self.root, 'prints'])
        self.templates  = '/'.join([self.root, 'templates'])
        self.pictures   = '/'.join([self.root, 'pictures'])
