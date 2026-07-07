import unittest
from evaluate import Evaluator
from htypes import Integer, Float


class TestLoops(unittest.TestCase):

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

    def test_for_basic_accumulation(self):
        script = """(defvar total 0)
                    (for i 0 (< i 10) (setq i (+ i 1))
                      (setq total (+ total i)))"""

        self.evaluate(script)
        self.assertEqual(self.evaluate("total"), Integer(45))

    def test_for_loop_variable_final_value(self):
        script = """(for i 0 (< i 10) (setq i (+ i 1))
                      (setq i i))"""

        self.evaluate(script)
        self.assertEqual(self.evaluate("i"), Integer(10))

    def test_for_condition_false_from_start_does_not_run_body(self):
        script = """(defvar hits 0)
                    (for i 10 (< i 0) (setq i (+ i 1))
                      (setq hits (+ hits 1)))"""
        
        self.evaluate(script)
        self.assertEqual(self.evaluate("hits"), Integer(0))

    def test_for_equal_bounds_does_not_run_body(self):
        script = """(defvar hits 0)
                    (for i 5 (< i 5) (setq i (+ i 1))
                      (setq hits (+ hits 1)))"""
        
        self.evaluate(script)
        self.assertEqual(self.evaluate("hits"), Integer(0))

    def test_for_single_iteration(self):
        script = """(defvar hits 0)
                    (for i 0 (< i 1) (setq i (+ i 1))
                      (setq hits (+ hits 1)))"""
        
        self.evaluate(script)
        self.assertEqual(self.evaluate("hits"), Integer(1))

    def test_for_multiple_body_expressions(self):
        script = """(defvar bigcount 0)
                    (defvar smallcount 0)
                    (for i 0 (< i 5) (setq i (+ i 1))
                      (setq bigcount (+ bigcount 2))
                      (setq smallcount (+ smallcount 1)))"""

        self.evaluate(script)
        self.assertEqual(self.evaluate("bigcount"), Integer(10))
        self.assertEqual(self.evaluate("smallcount"), Integer(5))

    def test_nested_for(self):
        script = """(defvar total 0)
                    (for i 0 (< i 3) (setq i (+ i 1))
                      (for j 0 (< j 3) (setq j (+ j 1))
                        (setq total (+ total 1))))"""

        self.evaluate(script)
        self.assertEqual(self.evaluate("total"), Integer(9))

    def test_for_custom_update_step(self):
        script = """(defvar total 0)
                    (for i 0 (< i 10) (setq i (+ i 2))
                      (setq total (+ total 1)))"""

        self.evaluate(script)
        self.assertEqual(self.evaluate("total"), Integer(5))

    def test_for_decrementing_update(self):
        script = """(defvar total 0)
                    (for i 5 (> i 0) (setq i (- i 1))
                      (setq total (+ total i)))"""

        self.evaluate(script)
        self.assertEqual(self.evaluate("total"), Integer(15))

    def test_for_negative_initval(self):
        script = """(defvar total 0)
                    (defvar hits 0)
                    (for i -3 (< i 3) (setq i (+ i 1))
                      (setq total (+ total i))
                      (setq hits (+ hits 1))"""

        self.evaluate(script)
        self.assertEqual(self.evaluate("total"), Integer(-3))
        self.assertEqual(self.evaluate("hits"), Integer(6))

    def test_for_body_references_outer_variable(self):
        script = """(defvar x 100)
                    (defvar total 0)
                    (for i 0 (< i 3) (setq i (+ i 1))
                      (setq total (+ total x)))"""

        self.evaluate(script)
        self.assertEqual(self.evaluate("total"), Integer(300))

    def test_for_float_initval(self):
        script = """(defvar total 0)
                    (for i 0.0 (< i 3) (setq i (+ i 1))
                      (setq total (+ total i)))"""

        self.evaluate(script)
        self.assertEqual(self.evaluate("total"), Float(3.0))

    def test_range_basic_accumulation(self):
        # sum 0..9 -> 45
        script = """(defvar total 0)
                    (range i 0 10
                        (setq total (+ total i)))"""
        self.evaluate(script)
        self.assertEqual(self.evaluate("total"), Integer(45))
        
    def test_range_loop_variable_final_value(self):
        # var itself should equal upper bound when loop exits
        script = """(range i 0 10
                      (setq i i))"""
        self.evaluate(script)
        self.assertEqual(self.evaluate("i"), Integer(10))
        
    def test_empty_range_does_not_run_body(self):
        # lower == upper -> body never executes
        script = """(defvar hits 0)
                    (range i 5 5
                      (setq hits (+ hits 1)))"""
        self.evaluate(script)
        self.assertEqual(self.evaluate("hits"), Integer(0))
        
    def test_inverted_range_does_not_run_body(self):
        # lower > upper -> condition false from the start
        script = """(defvar hits 0)
                    (range i 10 0
                      (setq hits (+ hits 1)))"""
        self.evaluate(script)
        self.assertEqual(self.evaluate("hits"), Integer(0))
        
    def test_single_iteration_range(self):
        script = """(defvar hits 0)
                    (range i 0 1
                      (setq hits (+ hits 1)))"""
        self.evaluate(script)
        self.assertEqual(self.evaluate("hits"), Integer(1))
        
    def test_range_multiple_body_expressions(self):
        # every expression in the &rest body should run, in order, each iteration
        script = """(defvar bigcount 0)
                    (defvar smallcount 0)
                    (range i 0 5
                      (setq bigcount (+ bigcount 2))
                      (setq smallcount (+ smallcount 1)))"""
        self.evaluate(script)
        self.assertEqual(self.evaluate("bigcount"), Integer(10))
        self.assertEqual(self.evaluate("smallcount"), Integer(5))
        
    def test_nested_range(self):
        # inner loop runs fully for each outer iteration
        script = """(defvar total 0)
                    (range i 0 3
                      (range j 0 3
                        (setq total (+ total 1))))"""
        self.evaluate(script)
        self.assertEqual(self.evaluate("total"), Integer(9))
        
    def test_range_body_references_outer_variable(self):
        script = """(defvar x 100)
                    (defvar total 0)
                    (range i 0 3
                      (setq total (+ total x)))"""
        self.evaluate(script)
        self.assertEqual(self.evaluate("total"), Integer(300))
        
    def test_negative_bounds_range(self):
        script = """(defvar total 0)
                    (range i -3 3
                      (setq total (+ total i)))"""
        self.evaluate(script)
        self.assertEqual(self.evaluate("total"), Integer(-3))
        
    def test_range_float_bounds(self):
        # loop variable increments by integer 1 each time, starting from a float
        script = """(defvar total 0)
                    (range i 0.0 3
                      (setq total (+ total i)))"""
        self.evaluate(script)
        self.assertEqual(self.evaluate("total"), Float(3.0))
        

if __name__ == "__main__":
    unittest.main()
