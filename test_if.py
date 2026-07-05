import unittest
from evaluate import Evaluator

class TestIf(unittest.TestCase):

    def setUp(self):
        self.evaluate = Evaluator().evaluate

    def test_then(self):
        self.assertEqual(self.evaluate("(if True 1 2)").value, 1)
        self.assertEqual(self.evaluate("(if \"Hello\" 1 2)").value, 1)

    def test_else(self):
        self.assertEqual(self.evaluate("(if False 1 2)").value, 2)

    def test_cond(self):
        self.assertEqual(self.evaluate("(if (< 1 2) 1 2)").value, 1)
        self.assertEqual(self.evaluate("(if (< 2 1) 1 2)").value, 2)

        self.assertEqual(self.evaluate("(if (> 2 1) 1 2)").value, 1)
        self.assertEqual(self.evaluate("(if (> 1 2) 1 2)").value, 2)

    def test_eval_then(self):
        self.assertEqual(self.evaluate("(if True (+ 1 2) (+ 2 3))").value, 3)

    def test_eval_else(self):
        self.assertEqual(self.evaluate("(if False (+ 1 2) (+ 2 3))").value, 5)


if __name__ == "__main__":
    unittest.main()
