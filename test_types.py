import unittest
from evaluate import Evaluator
from htypes import Nil, BooleanTrue


class TestTypes(unittest.TestCase):

    def setUp(self):
        self.evaluate = Evaluator().evaluate

    def tearDown(self):
        pass

    def test_atom(self):
        self.assertEqual(self.evaluate('(atom? 10)'), BooleanTrue())
        self.assertEqual(self.evaluate('(atom? 12.23)'), BooleanTrue())
        self.assertEqual(self.evaluate('(atom? "test")'), BooleanTrue())
        self.assertEqual(self.evaluate('(defvar x 10) (atom? x)'), BooleanTrue())

    def test_integer(self):
        self.assertEqual(self.evaluate('(int? 10)'), BooleanTrue())

    def test_float(self):
        self.assertEqual(self.evaluate('(float? 12.23)'), BooleanTrue())

    def test_string(self):
        self.assertEqual(self.evaluate('(string? "test")'), BooleanTrue())

    def test_symbol(self):
        self.assertEqual(self.evaluate('(defvar x 10) (symbol? (quote x))'), BooleanTrue())

    def test_num(self):
        self.assertEqual(self.evaluate("(num? 1)"), BooleanTrue())
        self.assertEqual(self.evaluate("(num? 1.1)"), BooleanTrue())
        self.assertEqual(self.evaluate('(num? "test")'), Nil())
        self.assertEqual(self.evaluate('(num? (< 1 2))'), Nil())
        self.assertEqual(self.evaluate('(num? (> 1 2))'), Nil())

if __name__ == "__main__":
    unittest.main()
