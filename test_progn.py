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

    def test_runs_every_expression(self):
        self.assertEqual(self.evaluate("(progn (setq x 10) (setq y 20) (+ x y))"), 30)

if __name__ == "__main__":
    unittest.main()
