import unittest
from evaluate import Evaluator
from htypes import String


class TestString(unittest.TestCase):

    def setUp(self):
        self.evaluate = Evaluator().evaluate

    def test_substring(self):
        self.evaluate("(defvar x \"test\")")
        self.assertEqual(self.evaluate("(substring x 0 2)"), String("\"te\""))
        self.assertEqual(self.evaluate("(substring x 1 2)"), String("\"e\""))

    def test_split_string_no_match(self):
        self.evaluate("(defvar x \"test\")")
        self.assertEqual(self.evaluate("(split-string x \"d\")"), [String("\"test\"")])

    def test_split_string_one_match(self):
        self.evaluate("(defvar x \"test\")")
        self.assertEqual(self.evaluate("(split-string x \"e\")"), [String("\"t\""), String("\"st\"")])

    def test_split_string_multiple_matches(self):
        self.evaluate("(defvar x \"test test\")")
        result = self.evaluate("(split-string x \"e\")")
        self.assertEqual(self.evaluate("(split-string x \"e\")"), [String("\"t\""), String("\"st t\""), String("\"st\"")])


if __name__ == "__main__":
    unittest.main()
