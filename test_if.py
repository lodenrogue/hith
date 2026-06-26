import unittest
from evaluate import Evaluator, variables

class TestIf(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.evaluate = Evaluator().evaluate

    def tearDown(self):
        variables.clear()

    def test_then(self):
        self.assertEqual(self.evaluate("(if True 1 2)"), 1)
        self.assertEqual(self.evaluate("(if \"Hello\" 1 2)"), 1)

    def test_else(self):
        self.assertEqual(self.evaluate("(if False 1 2)"), 2)

    def test_cond(self):
        self.assertEqual(self.evaluate("(if (< 1 2) 1 2)"), 1)
        self.assertEqual(self.evaluate("(if (< 2 1) 1 2)"), 2)

        self.assertEqual(self.evaluate("(if (> 2 1) 1 2)"), 1)
        self.assertEqual(self.evaluate("(if (> 1 2) 1 2)"), 2)

    def test_eval_then(self):
        self.assertEqual(self.evaluate("(if True (+ 1 2) (+ 2 3))"), 3)

    def test_eval_else(self):
        self.assertEqual(self.evaluate("(if False (+ 1 2) (+ 2 3))"), 5)


if __name__ == "__main__":
    unittest.main()
