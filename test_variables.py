import unittest
from evaluate import Evaluator, Env, Variables

class TestVariables(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.env = Env(variables=Variables(), parent=None)
        cls.evaluate = Evaluator(cls.env).evaluate

    def tearDown(self):
        self.env.clear_variables()

    def test_undefined_variable(self):
        self.assertEqual(self.evaluate("(symbol-value 'x)"), None)

    def test_defvar_variable_value(self):
        value = 20
        self.evaluate(f"(defvar x {value})")
        self.assertEqual(self.evaluate("x"), 20)

    def test_defvar_numeric_variable(self):
        value = 10
        self.evaluate(f"(defvar x {value})")
        self.assertEqual(self.evaluate("(symbol-value 'x)"), value)

    def test_defvar_string_variable(self):
        value = "\"Hello, world!\""
        self.evaluate(f"(defvar x {value})")
        self.assertEqual(self.evaluate("(symbol-value 'x)"), value)

    def test_defvar_return_variable_name(self):
        self.assertEqual(self.evaluate("(defvar test 10)"), "test")

    def test_setq_variable_value(self):
        value = 20
        self.evaluate(f"(setq x {value})")
        self.assertEqual(self.evaluate("x"), 20)

    def test_setq_numeric_variable(self):
        value = 10
        self.evaluate(f"(setq x {value})")
        self.assertEqual(self.evaluate("(symbol-value 'x)"), value)

    def test_setq_string_variable(self):
        value = "\"Hello, world!\""
        self.evaluate(f"(setq x {value})")
        self.assertEqual(self.evaluate("(symbol-value 'x)"), value)

    def test_setq_return_variable_name(self):
        self.assertEqual(self.evaluate("(setq test 10)"), "test")

if __name__ == "__main__":
    unittest.main()
