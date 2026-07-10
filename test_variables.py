import unittest
from evaluate import Evaluator
from htypes import NIL, Symbol, Integer, String


class TestVariables(unittest.TestCase):

    def setUp(self):
        self.evaluate = Evaluator().evaluate

    def test_undefined_variable(self):
        self.assertEqual(self.evaluate("(symbol-value 'x)"), NIL)

    def test_defvar_variable_value(self):
        value = 20
        self.evaluate(f'(defvar x {value})')
        self.assertEqual(self.evaluate("x").value, 20)

    def test_defvar_numeric_variable(self):
        value = 10
        self.evaluate(f'(defvar x {value})')
        self.assertEqual(self.evaluate('(symbol-value (quote x))'), Integer(value))

    def test_defvar_string_variable(self):
        value = '"Hello, world!"'
        self.evaluate(f'(defvar x {value})')
        self.assertEqual(self.evaluate('(symbol-value (quote x))'), String(value))

    def test_defvar_return_variable_name(self):
        self.assertEqual(self.evaluate('(defvar test 10)'), Symbol("test"))

    def test_setq_variable_value(self):
        value = 20
        self.evaluate(f'(setq x {value})')
        self.assertEqual(self.evaluate("x"), Integer(20))

    def test_setq_numeric_variable(self):
        value = 10
        self.evaluate(f'(setq x {value})')
        self.assertEqual(self.evaluate('(symbol-value (quote x))'), Integer(value))

    def test_setq_string_variable(self):
        value = '"Hello, world!"'
        self.evaluate(f'(setq x {value})')
        self.assertEqual(self.evaluate('(symbol-value (quote x))'), String(value))

    def test_setq_return_variable_name(self):
        self.assertEqual(self.evaluate('(setq test 10)'), Symbol("test"))

if __name__ == "__main__":
    unittest.main()
