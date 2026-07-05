import unittest
from evaluate import Evaluator
from htypes import Integer


class TestWhile(unittest.TestCase):

    def setUp(self):
        self.evaluate = Evaluator().evaluate

    def test_single_body_while(self):
        script = """(defvar count 0)
                    (while (< count 5)
                      (setq count (+ count 1)))"""

        self.evaluate(script)
        self.assertEqual(self.evaluate("count"), Integer(5))

    def test_multi_body_while(self):
        script = """(defvar count 0)
                    (defvar collect 10)

                    (while (< count 5)
                      (setq count (+ count 1))
                      (setq collect (+ collect 2)))"""

        self.evaluate(script)

        self.assertEqual(self.evaluate("count"), Integer(5))
        self.assertEqual(self.evaluate("collect"), Integer(20))
    

if __name__ == "__main__":
    unittest.main()
