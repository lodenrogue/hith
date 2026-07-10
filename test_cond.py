import unittest
from evaluate import Evaluator
from htypes import NIL, Integer


class TestCond(unittest.TestCase):

    def setUp(self):
        self.evaluate = Evaluator().evaluate

    def test_cond_no_clauses(self):
        self.assertEqual(self.evaluate('(cond (()))'), NIL)
        self.assertEqual(self.evaluate('(cond ())'), NIL)

    def test_cond_single_clause(self):
        self.assertEqual(self.evaluate('(cond ((> 2 1) 3))').value, 3)
        self.assertEqual(self.evaluate('(cond ((> 1 2) 3))'), NIL)

    def test_cond_multiple_clauses(self):
        script = """(defun check-value (x)
                      (cond
                        ((< x 0)  "X is negative")
                        ((eq x 0)  "X is zero")
                        ((eq x 1)  "X is exactly one")
                        (t        "X is something else (default case)")))"""

        self.evaluate(script)

        self.assertEqual(self.evaluate('(check-value -1)').value, '"X is negative"')
        self.assertEqual(self.evaluate('(check-value  0)').value, '"X is zero"')
        self.assertEqual(self.evaluate('(check-value  1)').value, '"X is exactly one"')
        self.assertEqual(self.evaluate('(check-value 10)').value, '"X is something else (default case)"')

if __name__ == "__main__":
    unittest.main()
