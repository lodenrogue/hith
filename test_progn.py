import unittest
from evaluate import Evaluator

class TestProgn(unittest.TestCase):

    def setUp(self):
        self.evaluate = Evaluator().evaluate

    def test_empty_body(self):
        self.assertEqual(self.evaluate("(progn)"), None)

    def test_single_expression(self):
        self.assertEqual(self.evaluate("(progn (+ 2 3))"), 5)

    def test_multi_expressions(self):
         self.assertEqual(self.evaluate("(progn (+ 2 3) (* 3 4))"), 12)


if __name__ == "__main__":
    unittest.main()
