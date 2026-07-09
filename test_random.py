import unittest
from evaluate import Evaluator
from htypes import Nil, Symbol


class TestRandom(unittest.TestCase):

    def setUp(self):
        self.evaluate = Evaluator().evaluate

    def test_random(self):
        self.assertTrue(self.evaluate("(float? (random))"))

    def test_random_range(self):
        self.assertTrue(self.evaluate("(int? (randrange 0 5)"))

    def test_random_choice_list(self):
        self.evaluate("(defvar x '())")
        self.assertEqual(self.evaluate("(choice x)"), Nil())

        self.evaluate("(defvar x '(a))")
        self.assertEqual(self.evaluate("(choice x)"), Symbol("a"))

        self.evaluate("(defvar x '(a b c))")
        self.assertTrue(self.evaluate("(choice x)") in [Symbol("a"), Symbol("b"), Symbol("c")])


if __name__ == "__main__":
    unittest.main()
