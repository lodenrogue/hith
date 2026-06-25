import unittest
from evaluate import evaluate, variables

class TestVariables(unittest.TestCase):

    def tearDown(self):
        variables.clear()

    def test_undefined_variable(self):
        self.assertEqual(evaluate("(symbol-value 'x)"), None)

    def test_variable_value(self):
        value = 20
        evaluate(f"(defvar x {value})")
        self.assertEqual(evaluate("x"), 20)

    def test_numeric_variable(self):
        value = 10
        evaluate(f"(defvar x {value})")
        self.assertEqual(evaluate("(symbol-value 'x)"), value)

    def test_string_variable(self):
        value = "\"Hello, world!\""
        evaluate(f"(defvar x {value})")
        self.assertEqual(evaluate("(symbol-value 'x)"), value)

if __name__ == "__main__":
    unittest.main()
