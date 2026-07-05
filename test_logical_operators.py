import unittest
from evaluate import Evaluator
from htypes import Boolean


class TestLogicalOperators(unittest.TestCase):

    def setUp(self):
        self.evaluate = Evaluator().evaluate

    def test_greater_than(self):
        self.assertEqual(self.evaluate("(> 2 1)"), Boolean(True))
        self.assertEqual(self.evaluate("(> 1 2)"), Boolean(False))
        self.assertEqual(self.evaluate("(> 2 2)"), Boolean(False))

    def test_greater_than_one_variable(self):
        self.evaluate("(defvar x 10)")
        self.assertEqual(self.evaluate("(> x 1)"), Boolean(True))
        self.assertEqual(self.evaluate("(> 1 x)"), Boolean(False))

    def test_greater_than_two_variables(self):
        self.evaluate("(defvar x 10)") 
        self.evaluate("(defvar y 20)")
        self.assertEqual(self.evaluate("(> x y)"), Boolean(False))
        self.assertEqual(self.evaluate("(> y x)"), Boolean(True))

    def test_less_than(self):
        self.assertEqual(self.evaluate("(< 1 2)"), Boolean(True))
        self.assertEqual(self.evaluate("(< 2 1)"), Boolean(False))
        self.assertEqual(self.evaluate("(< 2 2)"), Boolean(False))

    def test_less_than_variables(self):
        self.evaluate("(defvar x -5)")
        self.evaluate("(defvar y 0)")
        self.evaluate("(defvar z 5)")
        self.assertEqual(self.evaluate("(< x y)").value, True)
        self.assertEqual(self.evaluate("(< z y)").value, False)
        self.assertEqual(self.evaluate("(< x x)").value, False)

    def test_greater_than_or_equal(self):
        self.assertEqual(self.evaluate("(>= 2 1)").value, True)
        self.assertEqual(self.evaluate("(>= 2 2)").value, True)
        self.assertEqual(self.evaluate("(>= 1 2)"), Boolean(False))
        self.assertEqual(self.evaluate("(>= 0 -1)"), Boolean(True))
        self.assertEqual(self.evaluate("(>= -1 0)"), Boolean(False))
        self.assertEqual(self.evaluate("(>= -1 -1)"), Boolean(True))

    def test_greater_than_or_equal_variables(self):
        self.evaluate("(defvar x 10)")
        self.evaluate("(defvar y 10)")
        self.evaluate("(defvar z 5)")
        self.assertEqual(self.evaluate("(>= x y)"), Boolean(True))
        self.assertEqual(self.evaluate("(>= x z)"), Boolean(True))
        self.assertEqual(self.evaluate("(>= z x)"), Boolean(False))

    def test_less_than_or_equal(self):
        self.assertEqual(self.evaluate("(<= 1 2)"), Boolean(True))
        self.assertEqual(self.evaluate("(<= 2 2)"), Boolean(True))
        self.assertEqual(self.evaluate("(<= 2 1)"), Boolean(False))
        self.assertEqual(self.evaluate("(<= -2 -1)"), Boolean(True))
        self.assertEqual(self.evaluate("(<= -1 -2)"), Boolean(False))
        self.assertEqual(self.evaluate("(<= 0 0)"), Boolean(True))

    def test_less_than_or_equal_variables(self):
        self.evaluate("(defvar x 20)")
        self.evaluate("(defvar y 20)")
        self.evaluate("(defvar z 30)")
        self.assertEqual(self.evaluate("(<= x y)"), Boolean(True))
        self.assertEqual(self.evaluate("(<= x z)"), Boolean(True))
        self.assertEqual(self.evaluate("(<= z x)"), Boolean(False))

    def test_equal(self):
        self.assertEqual(self.evaluate("(eq 1 1)"), Boolean(True))
        self.assertEqual(self.evaluate("(eq 1 2)"), Boolean(False))
        self.assertEqual(self.evaluate("(eq -1 -1)"), Boolean(True))
        self.assertEqual(self.evaluate("(eq 0 0)"), Boolean(True))
        self.assertEqual(self.evaluate("(eq 0 1)"), Boolean(False))

    def test_equal_variables(self):
        self.evaluate("(defvar x 100)")
        self.evaluate("(defvar y 100)")
        self.evaluate("(defvar z 200)")
        self.assertEqual(self.evaluate("(eq x y)"), Boolean(True))
        self.assertEqual(self.evaluate("(eq x z)"), Boolean(False))
        self.assertEqual(self.evaluate("(eq z z)"), Boolean(True))

    def test_nested_expressions(self):
        self.evaluate("(defvar x 5)")
        self.evaluate("(defvar y 10)")
        self.assertEqual(self.evaluate("(eq (< x y) (> y x))"), Boolean(True))
        self.assertEqual(self.evaluate("(eq (<= x y) (>= x y))"), Boolean(False))
        
if __name__ == "__main__":
    unittest.main()
