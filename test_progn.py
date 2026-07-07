import unittest
from evaluate import Evaluator
from htypes import Nil, Integer


class TestProgn(unittest.TestCase):

    def setUp(self):
        self.evaluate = Evaluator().evaluate

    def test_empty_body(self):
        self.assertEqual(self.evaluate("(progn)"), Nil())

    def test_single_expression(self):
        self.assertEqual(self.evaluate("(progn (+ 2 3))"), Integer(5))

    def test_multi_expressions(self):
         self.assertEqual(self.evaluate("(progn (+ 2 3) (* 3 4))"), Integer(12))

    def test_runs_every_expression(self):
        self.assertEqual(self.evaluate("(progn (setq x 10) (setq y 20) (+ x y))"), Integer(30))

if __name__ == "__main__":
    unittest.main()
