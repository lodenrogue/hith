import unittest
from evaluate import Evaluator


class TestRandom(unittest.TestCase):

    def setUp(self):
        self.evaluate = Evaluator().evaluate

    def test_random(self):
        self.assertTrue(self.evaluate("(floatp (random))"))

    def test_random_range(self):
        self.assertTrue(self.evaluate("(intp (randrange 0 5)"))


if __name__ == "__main__":
    unittest.main()
