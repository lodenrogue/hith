import unittest
from evaluate import Evaluator
from htypes import BooleanTrue, Nil


class TestLogicalOperators(unittest.TestCase):

    def setUp(self):
        self.evaluate = Evaluator().evaluate

    def test_greater_than(self):
        self.assertEqual(self.evaluate("(> 2 1)"), BooleanTrue())
        self.assertEqual(self.evaluate("(> 1 2)"), Nil())
        self.assertEqual(self.evaluate("(> 2 2)"), Nil())

    def test_greater_than_one_variable(self):
        self.evaluate("(defvar x 10)")
        self.assertEqual(self.evaluate("(> x 1)"), BooleanTrue())
        self.assertEqual(self.evaluate("(> 1 x)"), Nil())

    def test_greater_than_two_variables(self):
        self.evaluate("(defvar x 10)") 
        self.evaluate("(defvar y 20)")
        self.assertEqual(self.evaluate("(> x y)"), Nil())
        self.assertEqual(self.evaluate("(> y x)"), BooleanTrue())

    def test_less_than(self):
        self.assertEqual(self.evaluate("(< 1 2)"), BooleanTrue())
        self.assertEqual(self.evaluate("(< 2 1)"), Nil())
        self.assertEqual(self.evaluate("(< 2 2)"), Nil())

    def test_less_than_variables(self):
        self.evaluate("(defvar x -5)")
        self.evaluate("(defvar y 0)")
        self.evaluate("(defvar z 5)")
        self.assertEqual(self.evaluate("(< x y)"), BooleanTrue())
        self.assertEqual(self.evaluate("(< z y)"), Nil())
        self.assertEqual(self.evaluate("(< x x)"), Nil())

    def test_greater_than_or_equal(self):
        self.assertEqual(self.evaluate("(>= 2 1)"), BooleanTrue())
        self.assertEqual(self.evaluate("(>= 2 2)"), BooleanTrue())
        self.assertEqual(self.evaluate("(>= 1 2)"), Nil())
        self.assertEqual(self.evaluate("(>= 0 -1)"), BooleanTrue())
        self.assertEqual(self.evaluate("(>= -1 0)"), Nil())
        self.assertEqual(self.evaluate("(>= -1 -1)"), BooleanTrue())

    def test_greater_than_or_equal_variables(self):
        self.evaluate("(defvar x 10)")
        self.evaluate("(defvar y 10)")
        self.evaluate("(defvar z 5)")
        self.assertEqual(self.evaluate("(>= x y)"), BooleanTrue())
        self.assertEqual(self.evaluate("(>= x z)"), BooleanTrue())
        self.assertEqual(self.evaluate("(>= z x)"), Nil())

    def test_less_than_or_equal(self):
        self.assertEqual(self.evaluate("(<= 1 2)"), BooleanTrue())
        self.assertEqual(self.evaluate("(<= 2 2)"), BooleanTrue())
        self.assertEqual(self.evaluate("(<= 2 1)"), Nil())
        self.assertEqual(self.evaluate("(<= -2 -1)"), BooleanTrue())
        self.assertEqual(self.evaluate("(<= -1 -2)"), Nil())
        self.assertEqual(self.evaluate("(<= 0 0)"), BooleanTrue())

    def test_less_than_or_equal_variables(self):
        self.evaluate("(defvar x 20)")
        self.evaluate("(defvar y 20)")
        self.evaluate("(defvar z 30)")
        self.assertEqual(self.evaluate("(<= x y)"), BooleanTrue())
        self.assertEqual(self.evaluate("(<= x z)"), BooleanTrue())
        self.assertEqual(self.evaluate("(<= z x)"), Nil())

    def test_equal(self):
        self.assertEqual(self.evaluate("(eq 1 1)"), BooleanTrue())
        self.assertEqual(self.evaluate("(eq 1 2)"), Nil())
        self.assertEqual(self.evaluate("(eq -1 -1)"), BooleanTrue())
        self.assertEqual(self.evaluate("(eq 0 0)"), BooleanTrue())
        self.assertEqual(self.evaluate("(eq 0 1)"), Nil())

    def test_equal_variables(self):
        self.evaluate("(defvar x 100)")
        self.evaluate("(defvar y 100)")
        self.evaluate("(defvar z 200)")
        self.assertEqual(self.evaluate("(eq x y)"), BooleanTrue())
        self.assertEqual(self.evaluate("(eq x z)"), Nil())
        self.assertEqual(self.evaluate("(eq z z)"), BooleanTrue())

    def test_nested_expressions(self):
        self.evaluate("(defvar x 5)")
        self.evaluate("(defvar y 10)")
        self.assertEqual(self.evaluate("(eq (< x y) (> y x))"), BooleanTrue())
        self.assertEqual(self.evaluate("(eq (<= x y) (>= x y))"), Nil())

    def test_not(self):
        self.assertEqual(self.evaluate("(not nil)"), BooleanTrue())
        self.assertEqual(self.evaluate("(not t)"), Nil())
        self.assertEqual(self.evaluate("(not (> 2 1))"), Nil())
        self.assertEqual(self.evaluate("(not (> 1 2))"), BooleanTrue())
        
if __name__ == "__main__":
    unittest.main()
