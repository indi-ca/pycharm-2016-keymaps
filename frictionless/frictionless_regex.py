__author__ = "Indika Piyasena"

import logging
import unittest
import re

from mappings.translate import Translate

logger = logging.getLogger(__name__)


class FrictionlessRegex:
    def __init__(self):
        pass

    def process(self):
        pass

    @staticmethod
    def replace_one_keystroke(source, fmap):
        # <keyboard-shortcut first-keystroke="control alt J" />
        pattern = r'<keyboard-shortcut first-keystroke=\"([a-zA-Z0-9_\s]*) ([a-zA-Z0-9_]*)\" />'
        regex = re.compile(pattern)

        return regex.sub(
            lambda match: '<keyboard-shortcut first-keystroke="{0} {1}" />'
            .format(
                match.group(1),
                fmap(match.group(2))
            ), source)


    @staticmethod
    def replace_two_keystrokes(source, fmap):
        pattern = r'<keyboard-shortcut first-keystroke=\"([a-zA-Z0-9_\s]*) ([a-zA-Z0-9_]*)\" second-keystroke="([a-zA-Z0-9_\s]*) ([a-zA-Z0-9_]*)" />'
        regex = re.compile(pattern)

        return regex.sub(
            lambda
                    match: '<keyboard-shortcut first-keystroke="{0} {1}" second-keystroke="{2} {3}" />'
            .format(
                match.group(1),
                fmap(match.group(2)),
                match.group(3),
                fmap(match.group(4))
            ), source)


class FrictionlessRegexTestCase(unittest.TestCase):
    def test_one_keystroke(self):
        fmap = Translate.map_to_qwerty
        keystroke = '<keyboard-shortcut first-keystroke="control alt J" />'
        result = FrictionlessRegex.replace_one_keystroke(keystroke, fmap)
        print result
        self.assertEqual(
            '<keyboard-shortcut first-keystroke="control alt C" />', result)

    def test_one_keystroke_with_two(self):
        fmap = Translate.map_to_qwerty
        keystroke = '<keyboard-shortcut first-keystroke="control alt J" />'
        result = FrictionlessRegex.replace_two_keystrokes(keystroke, fmap)
        print result
        self.assertEqual(
            '<keyboard-shortcut first-keystroke="control alt J" />', result)

    def test_one_keystroke_redundant(self):
        fmap = Translate.map_to_qwerty
        keystroke = '<action id="CommentByLineComment">'
        result = FrictionlessRegex.replace_one_keystroke(keystroke, fmap)
        print result
        self.assertEqual(
            '<action id="CommentByLineComment">', result)

    def test_two_keystrokes(self):
        fmap = Translate.map_to_qwerty
        keystroke = '<keyboard-shortcut first-keystroke="meta E" second-keystroke="meta R" />'
        result = FrictionlessRegex.replace_two_keystrokes(keystroke, fmap)
        print result
        self.assertEqual(
            '<keyboard-shortcut first-keystroke="meta D" second-keystroke="meta O" />',
            result)

    def test_two_keystrokes_with_one(self):
        fmap = Translate.map_to_qwerty
        keystroke = '<keyboard-shortcut first-keystroke="meta E" second-keystroke="meta R" />'
        result = FrictionlessRegex.replace_one_keystroke(keystroke, fmap)
        print result
        self.assertEqual(
            '<keyboard-shortcut first-keystroke="meta E" second-keystroke="meta R" />',
            result)

    def test_two_keystrokes_redundant(self):
        fmap = Translate.map_to_qwerty
        keystroke = '<action id="CommentByLineComment">'
        result = FrictionlessRegex.replace_two_keystrokes(keystroke, fmap)
        print result
        self.assertEqual(
            '<action id="CommentByLineComment">',
            result)


if __name__ == '__main__':
    print "Testing FrictionlessRegex in stand-alone-mode"
    unittest.main()

