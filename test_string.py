import unittest
from evaluate import Evaluator
from htypes import String, Integer, Float, NIL


class TestString(unittest.TestCase):

    def setUp(self):
        self.evaluate = Evaluator().evaluate

    def test_substring(self):
        self.evaluate('(defvar x "test")')
        self.assertEqual(self.evaluate('(substring x 0 2)'), String('"te"'))
        self.assertEqual(self.evaluate('(substring x 1 2)'), String('"e"'))

    def test_split_string_no_match(self):
        self.evaluate('(defvar x "test")')
        self.assertEqual(self.evaluate('(split-string x "d")'), [String('"test"')])

    def test_split_string_one_match(self):
        self.evaluate('(defvar x "test")')
        self.assertEqual(self.evaluate('(split-string x "e")'), [String('"t"'), String('"st"')])

    def test_split_string_multiple_matches(self):
        self.evaluate('(defvar x "test test")')
        self.assertEqual(self.evaluate('(split-string x "e")'), [String('"t"'), String('"st t"'), String('"st"')])

    def test_string_to_number_integer(self):
        self.assertEqual(self.evaluate('(string-to-number "10")'), Integer(10))

    def test_string_to_number_float(self):
        self.assertEqual(self.evaluate('(string-to-number "10.55")'), Float(10.55))

    def test_string_to_number_non_number(self):
        self.assertEqual(self.evaluate('(string-to-number "test")'), NIL)

    def test_char_to_ord(self):
        self.assertEqual(self.evaluate('(char-to-ord "A")'), Integer(65))
        self.assertEqual(self.evaluate('(char-to-ord "Hello")'), Integer(72))

    def test_ord_to_char(self):
        self.assertEqual(self.evaluate('(ord-to-char 65)'), String('"A"'))
        self.assertEqual(self.evaluate('(ord-to-char 72)'), String('"H"'))


if __name__ == "__main__":
    unittest.main()
