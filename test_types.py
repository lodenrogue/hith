import unittest
from evaluate import Evaluator
from htypes import NIL, T


class TestTypes(unittest.TestCase):

    def setUp(self):
        self.evaluate = Evaluator().evaluate

    def tearDown(self):
        pass

    def test_atom(self):
        self.assertEqual(self.evaluate('(atom? 10)'), T)
        self.assertEqual(self.evaluate('(atom? 12.23)'), T)
        self.assertEqual(self.evaluate('(atom? "test")'), T)
        self.assertEqual(self.evaluate('(defvar x 10) (atom? x)'), T)

    def test_integer(self):
        self.assertEqual(self.evaluate('(int? 10)'), T)

    def test_float(self):
        self.assertEqual(self.evaluate('(float? 12.23)'), T)

    def test_string(self):
        self.assertEqual(self.evaluate('(string? "test")'), T)

    def test_symbol(self):
        self.assertEqual(self.evaluate('(defvar x 10) (symbol? (quote x))'), T)

    def test_num(self):
        self.assertEqual(self.evaluate("(num? 1)"), T)
        self.assertEqual(self.evaluate("(num? 1.1)"), T)
        self.assertEqual(self.evaluate('(num? "test")'), NIL)
        self.assertEqual(self.evaluate('(num? (< 1 2))'), NIL)
        self.assertEqual(self.evaluate('(num? (> 1 2))'), NIL)

if __name__ == "__main__":
    unittest.main()
