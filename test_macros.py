import unittest
from evaluate import Evaluator
from htypes import Integer


class TestMacros(unittest.TestCase):

    def setUp(self):
        self.evaluate = Evaluator().evaluate

    def test_single_arg(self):
        self.evaluate("(defmacro test (arg) arg)")
        self.assertEqual(self.evaluate("(test 5)"), Integer(5))

    def test_multi_arg(self):
        self.evaluate("(defmacro test (arg1 arg2) (+ arg1 arg2))")
        self.assertEqual(self.evaluate("(test 5 10)"), Integer(15))

    def test_only_body(self):
        self.evaluate("(defmacro test (&rest body) `(progn ,@body))")
        self.assertEqual(self.evaluate("(test 5)"), Integer(5))

    def test_complex_macro_with_rest_and_splice(self):
        self.evaluate("""
            (defmacro my-when (test &rest body)
            `(if ,test (progn ,@body) False))
        """)
        self.evaluate("(defvar x 10)")
        result = self.evaluate("""
            (my-when (> x 5)
              (setq x (+ x 1))
              (setq x (* x 2))
              x)
        """)
        self.assertEqual(result, Integer(22))
        self.assertEqual(self.evaluate("(symbol-value 'x)"), Integer(22))

if __name__ == "__main__":
    unittest.main()
