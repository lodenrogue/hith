import unittest
from evaluate import Evaluator

class TestNth(unittest.TestCase):

    def setUp(self):
        self.evaluate = Evaluator().evaluate

    def test_empty_list(self):
        self.assertEqual(self.evaluate("(nth 0 (quote ()))"), None)

    def test_first_item(self):
        self.assertEqual(self.evaluate("(nth 0 (quote (123 456 789)))"), 123)

    def test_middle_item(self):
        self.assertEqual(self.evaluate("(nth 1 (quote (123 456 789)))"), 456)

    def test_last_item(self):
        self.assertEqual(self.evaluate("(nth 2 (quote (123 456 789)))"), 789)


if __name__ == "__main__":
    unittest.main()
