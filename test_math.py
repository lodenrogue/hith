import unittest
from evaluate import evaluate, variables

class TestMath(unittest.TestCase):

    def tearDown(self):
        variables.clear()

    def test_eval_number(self):
        self.assertEqual(evaluate("42"), 42)

    def test_eval_simple_sum(self):
        self.assertEqual(evaluate("(+ 1 2)"), 3)

    def test_eval_nested_sum(self):
        self.assertEqual(evaluate("(+ 1 (+ (+ 2.23 5) 3))"), 11.23)

    def test_sum_variables(self):
        evaluate("(defvar a 4)")
        evaluate("(defvar b 8)")
        self.assertEqual(evaluate("(+ a b)"), 12)
    
    def test_eval_simple_subtraction(self):
        self.assertEqual(evaluate("(- 1 2)"), -1)

    def test_eval_nested_subtraction(self):
        self.assertEqual(evaluate("(- 6 (- 4 2))"), 4)

    def test_eval_simple_multiplication(self):
        self.assertEqual(evaluate("(* 3 9)"), 27)

    def test_eval_nested_multiplication(self):
        self.assertEqual(evaluate("(* (* 3 4) 6)"), 72)

    def test_eval_simple_division(self):
        self.assertEqual(evaluate("(/ 27 3)"), 9)

    def test_eval_nested_division(self):
        self.assertEqual(evaluate("(/ 20 (/ 44 11))"), 5)

    def test_eval_mixed_math(self):
        self.assertEqual(evaluate("(* 3 (+ 4 (- 13 6)))"), 33)

if __name__ == "__main__":
    unittest.main()
