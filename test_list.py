import unittest
from evaluate import Evaluator
from htypes import Integer


class TestList(unittest.TestCase):

    def setUp(self):
        self.evaluate = Evaluator().evaluate

    def test_push(self):
        self.evaluate("(defvar list '(1 2 3))")
        self.assertEqual(self.evaluate("(push 0 list)"), [Integer(0), Integer(1), Integer(2), Integer(3)])

    def test_reverse(self):
        self.evaluate("(defvar list '(1 2 3))")
        self.assertEqual(self.evaluate("(reverse list)"), [Integer(3), Integer(2), Integer(1)])

    def test_append(self):
        self.evaluate("(defvar list '(1 2 3))")
        self.assertEqual(self.evaluate("(append 4 list)"), [Integer(1), Integer(2), Integer(3), Integer(4)])


if __name__ == "__main__":
    unittest.main()
