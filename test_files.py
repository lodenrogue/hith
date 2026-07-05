import os
import unittest
from evaluate import Evaluator
from htypes import String


TEST_FILE = "test.txt"

class TestFiles(unittest.TestCase):

    def setUp(self):
        self.evaluate = Evaluator().evaluate

    def tearDown(self):
        if os.path.exists(TEST_FILE):
            os.remove(TEST_FILE)

    def test_read_lines(self):
        with open(TEST_FILE, "a") as f:
            f.write("first\n")
            f.write("second\n")
            f.write("third\n")

        script = f"""(defvar file "{TEST_FILE}")
                    (file-read-lines file)"""

        self.assertEqual(self.evaluate(script), [String("first"), String("second"), String("third")])


if __name__ == "__main__":
    unittest.main()
