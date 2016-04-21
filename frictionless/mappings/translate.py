#!/usr/bin/env python

"""Translate

Translates keyboards


Usage:
   translate.py <target> <key>

Options:
    -h --help     Show this screen.
    --version     Show version.

"""
import unittest

__author__ = "Indika Piyasena"

import os
import logging

from docopt import docopt
from frictionless_map import frictionless as fmap

logger = logging.getLogger(__name__)


class Translate:
    def __init__(self):
        pass

    def map_keyboard(self, key, reverse=False):
        """

        :param key: The key to map
        :param reverse: The map maps by default QWERTY to Frictionless
        :return:
        """
        if not reverse:
            return fmap[key]
        else:
            return self.search(fmap, key)

    def process(self):
        self.configure_logging()

        global ret
        arguments = docopt(__doc__, version='Translate 0.1')
        logger.info('Translate started...')

        target = arguments['<target>']
        key = arguments['<key>']

        if target == 'frictionless':
            ret = self.map_keyboard(key, reverse=False)
        elif target == 'qwerty':
            ret = self.map_keyboard(key, reverse=True)
        else:
            logger.error('Invalid input')

        print ret

    @staticmethod
    def map_to_frictionless(key):
        if fmap.has_key(key):
            return fmap[key]
        else:
            return key

    @staticmethod
    def map_to_qwerty(key):
        result = Translate.search(fmap, key)
        if result:
            return result
        else:
            return key

    @staticmethod
    def search(key_dict, value):
        for name, age in key_dict.iteritems():
            if age == value:
                return name
        return None

    @staticmethod
    def configure_logging():
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        pass

    def log(self):
        pass


class TranslateTestCase(unittest.TestCase):
    def test_qwerty_to_frictionless(self):
        # h maps to d
        self.assertEqual('D', Translate.map_to_frictionless('H'))
        self.assertEqual('AWESOME', Translate.map_to_frictionless('AWESOME'))

    def test_friction_to_qwerty(self):
        # d maps to h
        self.assertEqual('H', Translate.map_to_qwerty('D'))
        self.assertEqual('AWESOME', Translate.map_to_qwerty('AWESOME'))


if __name__ == "__main__":
    print "Running Translate in stand-alone-mode"

    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    translate = Translate()
    translate.process()

