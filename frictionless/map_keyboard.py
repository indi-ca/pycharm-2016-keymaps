from frictionless_regex import FrictionlessRegex
from mappings.translate import Translate

__author__ = "Indika Piyasena"

import logging
import unittest

logger = logging.getLogger(__name__)


class MapKeyboardLayoutFile:
    def __init__(self):
        pass

    def translate(self, source_file, target_file, translator, fmap):
        with open(target_file, 'wb') as f:
            for line in self.source(source_file, translator):
                line = FrictionlessRegex.replace_one_keystroke(line, fmap)
                line = FrictionlessRegex.replace_two_keystrokes(line, fmap)
                f.write(line)

    def convert_to_windows(self, source_file, target_file):
        fmap = Translate.map_to_qwerty
        translator = MapKeyboardLayoutFile.translate_to_windows
        self.translate(source_file, target_file, translator, fmap)

    def convert_to_osx(self, source_file, target_file):
        fmap = Translate.map_to_frictionless
        translator = MapKeyboardLayoutFile.translate_to_osx
        self.translate(source_file, target_file, translator, fmap)

    @staticmethod
    def translate_to_windows(line):
        newline = line.replace("meta", "SWAP_VARIABLE")
        newline = newline.replace("control", "meta")
        newline = newline.replace("SWAP_VARIABLE", "control")
        newline = newline.replace("OSX-Pycharm-Frictionless",
                                  "Win-Pycharm-Frictionless")
        newline = newline.replace("Mac OS X 10.5+", "$default")
        return newline

    @staticmethod
    def translate_to_osx(line):
        newline = line.replace("control", "SWAP_VARIABLE")
        newline = newline.replace("meta", "control")
        newline = newline.replace("SWAP_VARIABLE", "meta")
        newline = newline.replace("Win-Pycharm-Frictionless",
                                  "OSX-Pycharm-Frictionless")
        newline = newline.replace("$default", "Mac OS X 10.5+")
        return newline


    @staticmethod
    def source(source_file, translator):
        with open(source_file, 'r') as f:
            for line in f:
                yield translator(line)


class MapKeyboardLayoutFileTestCase(unittest.TestCase):
    def test_windows_translation(self):
        win_file = 'data/Win_Pycharm_Frictionless.xml'
        osx_file = 'data/OSX_Pycharm_Frictionless.xml'

        win_file_target = 'data/Win_Pycharm_Frictionless_Target.xml'
        osx_file_target = 'data/OSX_Pycharm_Frictionless_Target.xml'

        lib = MapKeyboardLayoutFile()
        lib.convert_to_windows(osx_file, osx_file_target)
        self.assertEqual(True, True)

    def test_osx_translation(self):
        win_file = 'data/Win_Pycharm_Frictionless.xml'
        osx_file = 'data/OSX_Pycharm_Frictionless.xml'

        win_file_target = 'data/Win_Pycharm_Frictionless_Target.xml'
        osx_file_target = 'data/OSX_Pycharm_Frictionless_Target.xml'

        lib = MapKeyboardLayoutFile()
        lib.convert_to_osx(win_file, win_file_target)
        self.assertEqual(True, True)


if __name__ == '__main__':
    print "Testing MapKeyboardLayoutFile in stand-alone-mode"
    unittest.main()

