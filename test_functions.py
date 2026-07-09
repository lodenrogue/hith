import unittest
from evaluate import Evaluator, UndefinedFunctionException
from htypes import Integer


class TestFunctions(unittest.TestCase):

    def setUp(self):
        self.evaluate = Evaluator().evaluate

    def test_simple_function(self):
        self.evaluate("(defun add10 (a) (+ a 10))")
        self.assertEqual(self.evaluate("(add10 5)"), Integer(15))

    def test_global_vars_function(self):
        self.evaluate("(defun add20 (a) (+ a 20))")
        self.evaluate("(defvar x 10)")
        self.assertEqual(self.evaluate("(add20 x)"), Integer(30))

    def test_function_with_multiple_expressions(self):
        self.evaluate("""(defun multi-expressions (x y)
                           (setq total (+ x y))
                           (setq total (* total y))
                           (+ total y))""")

        self.assertEqual(self.evaluate("(multi-expressions 2 3)"), Integer(18))

    def test_nested_functions(self):
        self.evaluate("""(defun outer-func (x)
                           (defun inner-func (x) (+ x 1))
                           (+ x (inner-func 10)))""")

        self.assertEqual(self.evaluate("(outer-func 5)"), Integer(16))

    def test_function_scope(self):
        # Nested functions should not be visible from global scope
        self.evaluate("""(defun outer-func (n)
                           (defun inner-func (x) (+ x n))
                           (inner-func 5))""")

        with self.assertRaises(UndefinedFunctionException):
            self.evaluate("(inner-func 10)")

    def test_funcall_symbol(self):
        self.evaluate("(defun add10 (x) (+ x 10))")
        self.assertEqual(self.evaluate("(funcall add10 5)"), Integer(15))

    def test_funcall_variable(self):
        self.evaluate("(defvar my-op '+)")
        self.assertEqual(self.evaluate("(funcall my-op 1 2)"), Integer(3))


if __name__ == "__main__":
    unittest.main()
