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


if __name__ == "__main__":
    unittest.main()
