import unittest
from evaluate import Evaluator, variables

class TestVariables(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.evaluate = Evaluator().evaluate

    def tearDown(self):
        variables.clear()

    def test_undefined_variable(self):
        self.assertEqual(self.evaluate("(symbol-value 'x)"), None)

    def test_variable_value(self):
        value = 20
        self.evaluate(f"(defvar x {value})")
        self.assertEqual(self.evaluate("x"), 20)

    def test_numeric_variable(self):
        value = 10
        self.evaluate(f"(defvar x {value})")
        self.assertEqual(self.evaluate("(symbol-value 'x)"), value)

    def test_string_variable(self):
        value = "\"Hello, world!\""
        self.evaluate(f"(defvar x {value})")
        self.assertEqual(self.evaluate("(symbol-value 'x)"), value)

    def test_return_variable_name(self):
        self.assertEqual(self.evaluate("(defvar test 10)"), "test")

if __name__ == "__main__":
    unittest.main()
