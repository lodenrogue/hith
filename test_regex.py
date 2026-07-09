import unittest
import re
from evaluate import Evaluator
from htypes import Nil, Integer


class TestRegex(unittest.TestCase):

    def setUp(self):
        self.evaluate = Evaluator().evaluate

    def test_simple_regex(self):
        self.assertEqual(self.evaluate('(string-match "test" "e")'), Integer(1))

    def test_complex_regex(self):
        self.assertEqual(self.evaluate('(string-match "1d10" "^[0-9]+d[0-9]+([+-]?[0-9]+)?$")'), Integer(0))
        self.assertEqual(self.evaluate('(string-match "1d10+3" "^[0-9]+d[0-9]+([+-]?[0-9]+)?$")'), Integer(0))
        self.assertEqual(self.evaluate('(string-match "20d10-12" "^[0-9]+d[0-9]+([+-]?[0-9]+)?$")'), Integer(0))
        self.assertEqual(self.evaluate('(string-match "1d10xx" "^[0-9]+d[0-9]+([+-]?[0-9]+)?$")'), Nil())

    def test_string_match_found(self):
        self.evaluate('(defvar x "test")')
        self.assertEqual(self.evaluate('(string-match x "es")'), Integer(1))

    def test_string_match_not_found(self):
        self.evaluate('(defvar x "test")')
        self.assertEqual(self.evaluate('(string-match x "z")'), Nil())

    def test_string_match_literal_plus(self):
        # searching for a literal "+" requires escaping it in the pattern: \+
        self.evaluate('(defvar x "a+b")')
        self.assertEqual(self.evaluate('(string-match x "\\+")'), Integer(1))

    def test_string_match_literal_dot(self):
        self.evaluate('(defvar x "3.14")')
        self.assertEqual(self.evaluate('(string-match x "\\.")'), Integer(1))

    def test_string_match_literal_parens(self):
        self.evaluate('(defvar x "foo(bar)")')
        self.assertEqual(self.evaluate('(string-match x "\\(bar\\)")'), Integer(3))

    def test_string_match_unescaped_plus_raises(self):
        # "+" alone is not valid regex on its own (nothing to repeat)
        self.evaluate('(defvar x "a+b")')
        with self.assertRaises(re.error):
            self.evaluate('(string-match x "+")')

    def test_string_match_escaped_plus_literal(self):
        self.assertEqual(self.evaluate('(string-match "10+3" "\\+")'), Integer(2))


if __name__ == "__main__":
    unittest.main()
