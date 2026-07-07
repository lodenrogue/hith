import unittest
from evaluate import Evaluator
from htypes import Nil, Integer


class TestIf(unittest.TestCase):

    def setUp(self):
        self.evaluate = Evaluator().evaluate

    def test_then(self):
        self.assertEqual(self.evaluate("(if True 1 2)"), Integer(1))
        self.assertEqual(self.evaluate("(if \"Hello\" 1 2)"), Integer(1))

    def test_else(self):
        self.assertEqual(self.evaluate("(if False 1 2)"), Integer(2))

    def test_cond(self):
        self.assertEqual(self.evaluate("(if (< 1 2) 1 2)"), Integer(1))
        self.assertEqual(self.evaluate("(if (< 2 1) 1 2)"), Integer(2))

        self.assertEqual(self.evaluate("(if (> 2 1) 1 2)"), Integer(1))
        self.assertEqual(self.evaluate("(if (> 1 2) 1 2)"), Integer(2))

    def test_eval_then(self):
        self.assertEqual(self.evaluate("(if True (+ 1 2) (+ 2 3))"), Integer(3))

    def test_eval_else(self):
        self.assertEqual(self.evaluate("(if False (+ 1 2) (+ 2 3))"), Integer(5))

    def test_no_else(self):
        self.assertEqual(self.evaluate("(if False 1)"), Nil())


if __name__ == "__main__":
    unittest.main()
