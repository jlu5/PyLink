"""
Test cases for utils.py
"""

import unittest
from pylinkirc import utils

class UtilsTestCase(unittest.TestCase):

    def test_strip_irc_formatting(self):
        # Some messages from http://modern.ircdocs.horse/formatting.html#examples
        self.assertEqual(utils.strip_irc_formatting(
            "I love \x033IRC! \x03It is the \x037best protocol ever!"),
            "I love IRC! It is the best protocol ever!")

        self.assertEqual(utils.strip_irc_formatting(
            "This is a \x1d\x0313,9cool \x03message"),
            "This is a cool message")

        self.assertEqual(utils.strip_irc_formatting(
            "Don't spam 5\x0313,8,6\x03,7,8, and especially not \x029\x02\x1d!"),
            "Don't spam 5,6,7,8, and especially not 9!")

        # Should not remove the ,
        self.assertEqual(utils.strip_irc_formatting(
            "\x0305,"),
            ",")
        self.assertEqual(utils.strip_irc_formatting(
            "\x038,,,,."),
            ",,,,.")

        # Numbers are preserved
        self.assertEqual(utils.strip_irc_formatting(
            "\x031234 "),
            "34 ")
        self.assertEqual(utils.strip_irc_formatting(
            "\x03\x1f12"),
            "12")

        self.assertEqual(utils.strip_irc_formatting(
            "\x0305t\x030,1h\x0307,02e\x0308,06 \x0309,13q\x0303,15u\x0311,14i\x0310,05c\x0312,04k\x0302,07 \x0306,08b\x0313,09r\x0305,10o\x0304,12w\x0307,02n\x0308,06 \x0309,13f\x0303,15o\x0311,14x\x0310,05 \x0312,04j\x0302,07u\x0306,08m\x0313,09p\x0305,10s\x0304,12 \x0307,02o\x0308,06v\x0309,13e\x0303,15r\x0311,14 \x0310,05t\x0312,04h\x0302,07e\x0306,08 \x0313,09l\x0305,10a\x0304,12z\x0307,02y\x0308,06 \x0309,13d\x0303,15o\x0311,14g\x0f"),
            "the quick brown fox jumps over the lazy dog")

    def test_remove_range(self):
        self.assertEqual(utils.remove_range(
            "1", [1,2,3,4,5,6,7,8,9]),
            [2,3,4,5,6,7,8,9])

        self.assertEqual(utils.remove_range(
            "2,4", [1,2,3,4,5,6,7,8,9]),
            [1,3,5,6,7,8,9])

        self.assertEqual(utils.remove_range(
            "1-4", [1,2,3,4,5,6,7,8,9]),
            [5,6,7,8,9])

        self.assertEqual(utils.remove_range(
            "1-3,7", [1,2,3,4,5,6,7,8,9]),
            [4,5,6,8,9])

        self.assertEqual(utils.remove_range(
            "1-3,5-9", [1,2,3,4,5,6,7,8,9]),
            [4])

        self.assertEqual(utils.remove_range(
            "1-2,3-5,6-9", [1,2,3,4,5,6,7,8,9]),
            [])

        # Anti-patterns, but should be legal
        self.assertEqual(utils.remove_range(
            "4,2", [1,2,3,4,5,6,7,8,9]),
            [1,3,5,6,7,8,9])
        self.assertEqual(utils.remove_range(
            "4,4,4", [1,2,3,4,5,6,7,8,9]),
            [1,2,3,5,6,7,8,9])

        # Empty subranges should be filtered away
        self.assertEqual(utils.remove_range(
            ",2,,4,", [1,2,3,4,5,6,7,8,9]),
            [1,3,5,6,7,8,9])

        # Not enough items
        with self.assertRaises(IndexError):
            utils.remove_range(
                "5", ["abcd", "efgh"])
        with self.assertRaises(IndexError):
            utils.remove_range(
                "1-5", ["xyz", "cake"])

        # Ranges going in reverse or invalid
        with self.assertRaises(ValueError):
            utils.remove_range(
                "5-2", [":)", ":D", "^_^"])
            utils.remove_range(
                "2-2", [":)", ":D", "^_^"])

        # 0th element
        with self.assertRaises(ValueError):
            utils.remove_range(
                "5,0", list(range(50)))

        # List can't contain None
        with self.assertRaises(ValueError):
            utils.remove_range(
                "1-2", [None, "", 0, False])

        # Malformed indices
        with self.assertRaises(ValueError):
            utils.remove_range(
                " ", ["some", "clever", "string"])
            utils.remove_range(
                " ,,, ", ["some", "clever", "string"])
            utils.remove_range(
                "a,b,c,1,2,3", ["some", "clever", "string"])

        # Malformed ranges
        with self.assertRaises(ValueError):
            utils.remove_range(
                "1,2-", [":)", ":D", "^_^"])
            utils.remove_range(
                "-", [":)", ":D", "^_^"])
            utils.remove_range(
                "1-2-3", [":)", ":D", "^_^"])
            utils.remove_range(
                "-1-2", [":)", ":D", "^_^"])
            utils.remove_range(
                "3--", [":)", ":D", "^_^"])
            utils.remove_range(
                "--5", [":)", ":D", "^_^"])
            utils.remove_range(
                "-3--5", ["we", "love", "emotes"])

if __name__ == '__main__':
    unittest.main()