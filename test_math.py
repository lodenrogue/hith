import unittest
from evaluate import Evaluator
from htypes import Integer, Float


class TestMath(unittest.TestCase):

    def setUp(self):
        self.evaluate = Evaluator().evaluate

    def test_number(self):
        self.assertEqual(self.evaluate("42"), Integer(42))

    def test_simple_sum(self):
        self.assertEqual(self.evaluate("(+ 1 2)"), Integer(3))

    def test_nested_sum(self):
        self.assertEqual(self.evaluate("(+ 1 (+ (+ 2.23 5) 3))"), Float(11.23))

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

    def test_modulo(self):
        self.assertTrue(self.evaluate("(int? (mod 10 3))"))
        self.assertEqual(self.evaluate("(mod 10 3)").value, 1)
        self.assertEqual(self.evaluate("(mod 12 4)").value, 0)
        self.assertEqual(self.evaluate("(mod 3 10)").value, 3)
        self.assertEqual(self.evaluate("(mod 0 5)").value, 0)

        self.assertEqual(self.evaluate("(mod -5 3)").value, 1)
        self.assertEqual(self.evaluate("(mod 5 -3)").value, -1)
        self.assertEqual(self.evaluate("(mod -5 -3)").value, -2)

        self.assertEqual(self.evaluate("(mod 5.5 2)").value, 1.5)
        self.assertEqual(self.evaluate("(mod 0.5 1.5)").value, 0.5)
        self.assertEqual(self.evaluate("(mod -5.5 2)").value, 0.5)
        self.assertEqual(self.evaluate("(mod 5.5 -2.0)").value, -0.5)


if __name__ == "__main__":
    unittest.main()
