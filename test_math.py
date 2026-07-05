import unittest
from evaluate import Evaluator

class TestMath(unittest.TestCase):

    def setUp(self):
        self.evaluate = Evaluator().evaluate

    def test_number(self):
        self.assertEqual(self.evaluate("42").value, 42)

    def test_simple_sum(self):
        self.assertEqual(self.evaluate("(+ 1 2)").value, 3)

    def test_nested_sum(self):
        self.assertEqual(self.evaluate("(+ 1 (+ (+ 2.23 5) 3))").value, 11.23)

    def test_sum_variables(self):
        self.evaluate("(defvar a 4)")
        self.evaluate("(defvar b 8)")
        self.assertEqual(self.evaluate("(+ a b)").value, 12)
    
    def test_simple_subtraction(self):
        self.assertEqual(self.evaluate("(- 1 2)").value, -1)

    def test_nested_subtraction(self):
        self.assertEqual(self.evaluate("(- 6 (- 4 2))").value, 4)

    def test_subtract_variables(self):
        self.evaluate("(defvar a 4)")
        self.evaluate("(defvar b 8)")
        self.assertEqual(self.evaluate("(- a b)").value, -4)

    def test_simple_multiplication(self):
        self.assertEqual(self.evaluate("(* 3 9)").value, 27)

    def test_multiply_variables(self):
        self.evaluate("(defvar a 4)")
        self.evaluate("(defvar b 8)")
        self.assertEqual(self.evaluate("(* a b)").value, 32)

    def test_nested_multiplication(self):
        self.assertEqual(self.evaluate("(* (* 3 4) 6)").value, 72)

    def test_simple_division(self):
        self.assertEqual(self.evaluate("(/ 27 3)").value, 9)

    def test_divide_variables(self):
        self.evaluate("(defvar a 4)")
        self.evaluate("(defvar b 8)")
        self.assertEqual(self.evaluate("(- b a)").value, 4)

    def test_nested_division(self):
        self.assertEqual(self.evaluate("(/ 20 (/ 44 11))").value, 5)

    def test_mixed_math(self):
        self.assertEqual(self.evaluate("(* 3 (+ 4 (- 13 6)))").value, 33)

    def test_mixed_math_with_variables(self):
        self.evaluate("(defvar a 4)")
        self.evaluate("(defvar b 8)")
        self.evaluate("(defvar c 10)")
        self.assertEqual(self.evaluate("(* a (+ b (- c a)))").value, 56)


if __name__ == "__main__":
    unittest.main()
