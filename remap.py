#!/usr/bin/python

"""Remap

Remaps Python keyboard mapping files between OSX and Windows

Usage:
   remap.py
   remap.py to_osx
   remap.py to_windows

Options:
    -h --help     Show this screen.
    --version     Show version.

"""

__author__ = "Indika Piyasena"

import os
import sys
import glob
import logging
from docopt import docopt

logger = logging.getLogger(__name__)


def mtime(filename):
    return os.stat(filename).st_mtime

def atime(filename):
    return os.stat(filename).st_atime


class Remap:
    def __init__(self):
        self.configure_logging()
        self.win_file = 'Win_Pycharm_Frictionless.xml'
        self.osx_file = 'OSX_Pycharm_Frictionless.xml'

    def process(self):
        self.arguments = docopt(__doc__, version='Remap 0.1')
        if self.arguments['to_osx']:
            logger.info('Converting Windows -> OSX')
        elif self.arguments['to_windows']:
            logger.info('Converting OSX -> Windows')
            # set the windows file timestamp to the osx one
            last_modified_time = mtime(self.osx_file)
            last_access_time = atime(self.osx_file)
            self.regenerate_windows(last_access_time, last_modified_time)
        else:
            logger.info('Determining translation path from date modified...')
        return
        self.last_file_updated()
        pass

    def last_file_updated(self):
        query = '*.xml'
        keymap_files = glob.glob(query)

        sorted_files = sorted(keymap_files, key=mtime, reverse=1)
        last_modified_file = sorted_files[0]
        second_last_modified_file = sorted_files[1]

        t1 = mtime(last_modified_file)
        t2 = mtime(second_last_modified_file)

        logger.debug('Last modified time: {0}'.format(t1))
        logger.debug('Second Last modified time: {0}'.format(t2))

        last_modified_time = mtime(last_modified_file)
        last_access_time = atime(last_modified_file)

        if sys.platform == "win32":
            logger.info('Detected Windows environment')
            self.regenerate_osx(last_access_time, last_modified_time)
        elif sys.platform == 'darwin':
            logger.info('Detected OSX environment')
            self.regenerate_windows(last_access_time, last_modified_time)
        else:
            logger.error('Unhandled platform: {0}'.format(sys.platform))
        pass

    def regenerate_windows(self, with_access_timestamp,
                           with_modified_timestamp):
        logger.info('Generating Windows Configuration File')
        logger.info('aka... converting OSX -> Windows')

        if os.path.exists(self.win_file):
            os.unlink(self.win_file)

        with open(self.win_file, 'w') as w:
            with open(self.osx_file, 'r') as f:
                for line in f:
                    newline = line.replace("meta", "SWAP_VARIABLE")
                    newline = newline.replace("control", "meta")
                    newline = newline.replace("SWAP_VARIABLE", "control")
                    newline = newline.replace("OSX-Pycharm-Frictionless",
                                              "Win-Pycharm-Frictionless")
                    newline = newline.replace("Mac OS X 10.5+", "$default")
                    w.write(newline)

        os.utime(self.win_file,
                 (with_access_timestamp, with_modified_timestamp))

    def regenerate_osx(self, with_access_timestamp, with_modified_timestamp):
        logger.info('Generating OSX Configuration File')
        logger.info('aka... converting Windows -> OSX')

        if os.path.exists(self.osx_file):
            os.unlink(self.osx_file)

        with open(self.osx_file, 'w') as w:
            with open(self.win_file, 'r') as f:
                for line in f:
                    newline = line.replace("control", "SWAP_VARIABLE")
                    newline = newline.replace("meta", "control")
                    newline = newline.replace("SWAP_VARIABLE", "meta")
                    newline = newline.replace("Win-Pycharm-Frictionless",
                                              "OSX-Pycharm-Frictionless")
                    newline = newline.replace("$default", "Mac OS X 10.5+")
                    w.write(newline)

        os.utime(self.osx_file,
                 (with_access_timestamp, with_modified_timestamp))


    def change_keys(self):
        #first start with finding all the appropriate occurences in the file


        pass

    def configure_logging(self):
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        pass


if __name__ == "__main__":
    print "Running Remap in stand-alone-mode"
    remap = Remap()
    remap.process()
