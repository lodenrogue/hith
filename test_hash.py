import os
import unittest
from evaluate import Evaluator
from htypes import String, T

class TestMap(unittest.TestCase):

    def setUp(self):
        self.evaluate = Evaluator().evaluate

    def test_hash(self):
        self.assertEqual(self.evaluate('(int? (hash "hello"))'), T)

        self.assertEqual(self.evaluate('(hash "")'), self.evaluate('(hash "")'))
        self.assertEqual(self.evaluate('(hash "t")'), self.evaluate('(hash "t")'))

        self.assertEqual(self.evaluate('(hash "test")'), self.evaluate('(hash "test")'))
        self.assertNotEqual(self.evaluate('(hash "test")'), self.evaluate('(hash "test1")'))

        self.assertNotEqual(self.evaluate('(hash "cat")'), self.evaluate('(hash "act")'))


if __name__ == "__main__":
    unittest.main()
