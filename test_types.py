import unittest
from evaluate import Evaluator


class TestTypes(unittest.TestCase):

    def setUp(self):
        self.evaluate = Evaluator().evaluate

    def tearDown(self):
        pass

    def test_atom(self):
        self.assertTrue(self.evaluate("(atom 10)"))
        self.assertTrue(self.evaluate("(atom 12.23)"))
        self.assertTrue(self.evaluate("(atom \"test\")"))

    def test_integer(self):
        self.assertTrue(self.evaluate("(intp 10)"))

    def test_float(self):
        self.assertTrue(self.evaluate("(floatp 12.23)"))

    def test_string(self):
        self.assertTrue(self.evaluate("(stringp \"test\")"))
        

if __name__ == "__main__":
    unittest.main()
