import unittest
from evaluate import Evaluator
from htypes import Nil, Integer


class TestRegex(unittest.TestCase):

    def setUp(self):
        self.evaluate = Evaluator().evaluate

    def test_simple_regex(self):
        self.assertEqual(self.evaluate("(string-match \"e\" \"test\")"), Integer(1))

    def test_complex_regex(self):
        self.assertEqual(self.evaluate("(string-match \"^[0-9]+d[0-9]+([+-]?[0-9]+)?$\" \"1d10\")"), Integer(0))
        self.assertEqual(self.evaluate("(string-match \"^[0-9]+d[0-9]+([+-]?[0-9]+)?$\" \"1d10+3\")"), Integer(0))
        self.assertEqual(self.evaluate("(string-match \"^[0-9]+d[0-9]+([+-]?[0-9]+)?$\" \"20d10-12\")"), Integer(0))
        self.assertEqual(self.evaluate("(string-match \"^[0-9]+d[0-9]+([+-]?[0-9]+)?$\" \"1d10xx\")"), Nil())

if __name__ == "__main__":
    unittest.main()
