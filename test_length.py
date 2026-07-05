import unittest
from evaluate import Evaluator
from htypes import Integer


class TestLength(unittest.TestCase):

    def setUp(self):
        self.evaluate = Evaluator().evaluate

    def test_string_length(self):
        self.assertEqual(self.evaluate("(length \"\")"), Integer(0))
        self.assertEqual(self.evaluate("(length \"a\")"), Integer(1))
        self.assertEqual(self.evaluate("(length \"ab\")"), Integer(2))
        self.assertEqual(self.evaluate("(length \"ab cd\")"), Integer(5))

        self.evaluate("(defvar x \"hello\")")
        self.assertEqual(self.evaluate("(length x)"), Integer(5))


    def test_list_length(self):
        self.assertEqual(self.evaluate("(length (quote (test 123)))"), Integer(2))


if __name__ == "__main__":
    unittest.main()
