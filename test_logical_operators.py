import unittest
from evaluate import Evaluator
from htypes import BooleanTrue, Nil, Integer


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

    def test_unless(self):
        self.assertEqual(self.evaluate("(unless t 1)"), Nil())
        self.assertEqual(self.evaluate("(unless nil 1)"), Integer(1))
        self.assertEqual(self.evaluate("(unless (> 2 1) 1)"), Nil())
        self.assertEqual(self.evaluate("(unless (> 1 2) 1)"), Integer(1))
        self.assertEqual(self.evaluate("(unless (> 1 2) (+ 3 2))"), Integer(5))

        script = """(unless (> 1 2)
                        (defvar x 10)
                        (setq x (+ x 2))
                        (setq x (+ x 2))
                        x)"""

        self.assertEqual(self.evaluate(script), Integer(14))

    def test_when(self):
        self.assertEqual(self.evaluate("(when t 1)"), Integer(1))
        self.assertEqual(self.evaluate("(when nil 1)"), Nil())
        self.assertEqual(self.evaluate("(when (> 2 1) 1)"), Integer(1))
        self.assertEqual(self.evaluate("(when (> 1 2) 1)"), Nil())
        self.assertEqual(self.evaluate("(when (> 2 1) (+ 3 2))"), Integer(5))

        script = """(when (> 2 1)
                        (defvar x 10)
                        (setq x (+ x 2))
                        (setq x (+ x 2))
                        x)"""

        self.assertEqual(self.evaluate(script), Integer(14))

    def test_and(self):
        self.assertEqual(self.evaluate("(and)"), BooleanTrue())
        self.assertEqual(self.evaluate("(and nil)"), Nil())
        self.assertEqual(self.evaluate("(and (> 2 3))"), Nil())
        self.assertEqual(self.evaluate("(and t)"), BooleanTrue())
        self.assertEqual(self.evaluate("(and t 1)"), Integer(1))
        self.assertEqual(self.evaluate("(and t 1 (+ 2 3))"), Integer(5))
        self.assertEqual(self.evaluate("(and t nil (+ 2 3))"), Nil())

    def test_or(self):
        self.assertEqual(self.evaluate("(or)"), Nil())
        self.assertEqual(self.evaluate("(or (> 2 1)"), BooleanTrue())
        self.assertEqual(self.evaluate("(or (> 1 1) (+ 1 2))"), Integer(3))
        self.assertEqual(self.evaluate("(or (> 1 1) (> 1 1))"), Nil())

        
if __name__ == "__main__":
    unittest.main()
