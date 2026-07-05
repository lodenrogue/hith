import unittest
from evaluate import Evaluator
from htypes import Symbol, Integer


class TestQuote(unittest.TestCase):

    def setUp(self):
        self.evaluate = Evaluator().evaluate

    def test_symbol(self):
        self.assertEqual(self.evaluate("(quote test)"), Symbol("test"))

    def test_list(self):
        self.assertEqual(self.evaluate("(quote (test 123))"), [Symbol("test"), Integer(123)])


if __name__ == "__main__":
    unittest.main()
