import unittest
from evaluate import Evaluator


class TestTypes(unittest.TestCase):

    def setUp(self):
        self.evaluate = Evaluator().evaluate

    def tearDown(self):
        pass

    def test_atom(self):
        self.assertTrue(self.evaluate('(atom 10)'))
        self.assertTrue(self.evaluate('(atom 12.23)'))
        self.assertTrue(self.evaluate('(atom "test")'))
        self.assertTrue(self.evaluate('(defvar x 10) (atom x)'))

    def test_integer(self):
        self.assertTrue(self.evaluate('(intp 10)'))

    def test_float(self):
        self.assertTrue(self.evaluate('(floatp 12.23)'))

    def test_string(self):
        self.assertTrue(self.evaluate('(stringp "test")'))

    def test_symbol(self):
        self.assertTrue(self.evaluate('(defvar x 10) (symbolp (quote x))'))

if __name__ == "__main__":
    unittest.main()
