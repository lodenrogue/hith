import unittest
from evaluate import Evaluator
from htypes import Nil, Integer, String


class TestNth(unittest.TestCase):

    def setUp(self):
        self.evaluate = Evaluator().evaluate

    def test_empty_list(self):
        self.assertEqual(self.evaluate("(nth 0 (quote ()))"), Nil())

    def test_first_item(self):
        self.assertEqual(self.evaluate("(nth 0 (quote (123 456 789)))"), Integer(123))

    def test_middle_item(self):
        self.assertEqual(self.evaluate("(nth 1 (quote (123 456 789)))"), Integer(456))

    def test_last_item(self):
        self.assertEqual(self.evaluate("(nth 2 (quote (123 456 789)))"), Integer(789))

    def test_string(self):
        self.assertEqual(self.evaluate("(nth 2 \"test\")"), String("s"))

if __name__ == "__main__":
    unittest.main()
