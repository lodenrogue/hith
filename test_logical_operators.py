import unittest
from evaluate import Evaluator

class TestLogicalOperators(unittest.TestCase):

    def setUp(self):
        self.evaluate = Evaluator().evaluate

    def test_greater_than(self):
        self.assertEqual(self.evaluate("(> 2 1)"), True)
        self.assertEqual(self.evaluate("(> 1 2)"), False)
        self.assertEqual(self.evaluate("(> 2 2)"), False)

    def test_greater_than_one_variable(self):
        self.evaluate("(defvar x 10)")
        self.assertEqual(self.evaluate("(> x 1)"), True)
        self.assertEqual(self.evaluate("(> 1 x)"), False)

    def test_greater_than_two_variables(self):
        self.evaluate("(defvar x 10)") 
        self.evaluate("(defvar y 20)")
        self.assertEqual(self.evaluate("(> x y)"), False)
        self.assertEqual(self.evaluate("(> y x)"), True)

    def test_less_than(self):
        self.assertEqual(self.evaluate("(< 1 2)"), True)
        self.assertEqual(self.evaluate("(< 2 1)"), False)
        self.assertEqual(self.evaluate("(< 2 2)"), False)

    def test_less_than_variables(self):
        self.evaluate("(defvar x -5)")
        self.evaluate("(defvar y 0)")
        self.evaluate("(defvar z 5)")
        self.assertEqual(self.evaluate("(< x y)"), True)
        self.assertEqual(self.evaluate("(< z y)"), False)
        self.assertEqual(self.evaluate("(< x x)"), False)

    def test_greater_than_or_equal(self):
        self.assertEqual(self.evaluate("(>= 2 1)"), True)
        self.assertEqual(self.evaluate("(>= 2 2)"), True)
        self.assertEqual(self.evaluate("(>= 1 2)"), False)
        self.assertEqual(self.evaluate("(>= 0 -1)"), True)
        self.assertEqual(self.evaluate("(>= -1 0)"), False)
        self.assertEqual(self.evaluate("(>= -1 -1)"), True)

    def test_greater_than_or_equal_variables(self):
        self.evaluate("(defvar x 10)")
        self.evaluate("(defvar y 10)")
        self.evaluate("(defvar z 5)")
        self.assertEqual(self.evaluate("(>= x y)"), True)
        self.assertEqual(self.evaluate("(>= x z)"), True)
        self.assertEqual(self.evaluate("(>= z x)"), False)

    def test_less_than_or_equal(self):
        self.assertEqual(self.evaluate("(<= 1 2)"), True)
        self.assertEqual(self.evaluate("(<= 2 2)"), True)
        self.assertEqual(self.evaluate("(<= 2 1)"), False)
        self.assertEqual(self.evaluate("(<= -2 -1)"), True)
        self.assertEqual(self.evaluate("(<= -1 -2)"), False)
        self.assertEqual(self.evaluate("(<= 0 0)"), True)

    def test_less_than_or_equal_variables(self):
        self.evaluate("(defvar x 20)")
        self.evaluate("(defvar y 20)")
        self.evaluate("(defvar z 30)")
        self.assertEqual(self.evaluate("(<= x y)"), True)
        self.assertEqual(self.evaluate("(<= x z)"), True)
        self.assertEqual(self.evaluate("(<= z x)"), False)

    def test_equal(self):
        self.assertEqual(self.evaluate("(eq 1 1)"), True)
        self.assertEqual(self.evaluate("(eq 1 2)"), False)
        self.assertEqual(self.evaluate("(eq -1 -1)"), True)
        self.assertEqual(self.evaluate("(eq 0 0)"), True)
        self.assertEqual(self.evaluate("(eq 0 1)"), False)

    def test_equal_variables(self):
        self.evaluate("(defvar x 100)")
        self.evaluate("(defvar y 100)")
        self.evaluate("(defvar z 200)")
        self.assertEqual(self.evaluate("(eq x y)"), True)
        self.assertEqual(self.evaluate("(eq x z)"), False)
        self.assertEqual(self.evaluate("(eq z z)"), True)

    def test_nested_expressions(self):
        self.evaluate("(defvar x 5)")
        self.evaluate("(defvar y 10)")
        self.assertEqual(self.evaluate("(eq (< x y) (> y x))"), True)
        self.assertEqual(self.evaluate("(eq (<= x y) (>= x y))"), False)
        
if __name__ == "__main__":
    unittest.main()
