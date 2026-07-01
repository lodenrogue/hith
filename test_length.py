import unittest
from evaluate import Evaluator

class TestLength(unittest.TestCase):

    def setUp(self):
        self.evaluate = Evaluator().evaluate

    def test_string_length(self):
        self.assertEqual(self.evaluate("(length \"\")"), 0)
        self.assertEqual(self.evaluate("(length \"a\")"), 1)
        self.assertEqual(self.evaluate("(length \"ab\")"), 2)
        self.assertEqual(self.evaluate("(length \"ab cd\")"), 5)

        self.evaluate("(defvar x \"hello\")")
        self.assertEqual(self.evaluate("(length x)"), 5)


    # def test_list_length(self):
    #     self.assertEqual(self.evaluate("(length '(test 123))"), 2)


if __name__ == "__main__":
    unittest.main()
