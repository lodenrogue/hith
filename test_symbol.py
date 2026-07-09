import unittest
from evaluate import Evaluator
from htypes import Symbol


class TestSymbol(unittest.TestCase):

    def setUp(self):
        self.evaluate = Evaluator().evaluate

    def test_make_symbol(self):
        result = self.evaluate('(make-symbol "x")')
        self.assertTrue(isinstance(result, Symbol))
        self.assertEqual(result.value, "x")

    def test_gensym(self):
        self.assertTrue(self.evaluate('(symbol? (gensym))'))
        self.assertEqual(self.evaluate('(gensym)').value, "#:G1")
        self.assertEqual(self.evaluate('(gensym)').value, "#:G2")
        self.assertEqual(self.evaluate('(gensym)').value, "#:G3")


if __name__ == "__main__":
    unittest.main()
