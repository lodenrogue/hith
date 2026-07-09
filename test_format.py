import unittest
from evaluate import Evaluator
from htypes import String


class TestFormat(unittest.TestCase):

    def setUp(self):
        self.evaluate = Evaluator().evaluate

    def test_format_no_arguments(self):
        self.assertEqual(self.evaluate('(format "test")'),
                         String('"test"'))

    def test_format_string_argument(self):
        self.assertEqual(self.evaluate('(format "test %s test" "value")'),
                         String('"test value test"'))

    def test_format_expression_argument(self):
        self.assertEqual(self.evaluate('(format "test %s test" (+ 1 2))'),
                         String('"test 3 test"'))

    def test_format_boolean(self):
        self.assertEqual(self.evaluate('(format "%s" t)'),
                         String('"t"'))

        self.assertEqual(self.evaluate('(format "%s" (< 1 2))'),
                         String('"t"'))

    def test_format_mixed_arguments(self):
        self.assertEqual(self.evaluate('(format "test %s test%s" (+ 1 2) "!!!")'),
                         String('"test 3 test!!!"'))


if __name__ == "__main__":
    unittest.main()
