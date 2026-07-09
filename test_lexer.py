import unittest
from lexer import Lexer

PRIMITIVE_EXAMPLE = "42"
SIMPLE_EXAMPLE = "(+ 1 2.3)"
COMPLEX_EXAMPLE = "(if (> x (+ 1.33 5.7)) (* x 2) 0)"
SPACES_EXAMPLE = '(defvar x "hello() 33.23 world")'

class TestLexer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.lexer = Lexer()

    def test_lexer_primitive(self):
        self.assertEqual(self.lexer.tokenize(PRIMITIVE_EXAMPLE), ["42"])

    def test_lexer_simple(self):
        self.assertEqual(self.lexer.tokenize(SIMPLE_EXAMPLE), ['(', '+', '1', '2.3', ')'])
        
    def test_lexer_complex(self):
        self.assertEqual(
            self.lexer.tokenize(COMPLEX_EXAMPLE), 
            ["(", "if", "(", ">", "x", "(", "+", "1.33", "5.7", ")", ")", "(", "*", "x", "2", ")", "0", ")"]
        )

    def test_lexer_with_spaces(self):
        self.assertEqual(self.lexer.tokenize(SPACES_EXAMPLE), ["(", "defvar", "x", '"hello() 33.23 world"', ")"])

    def test_lexer_newlines(self):
        self.assertEqual(self.lexer.tokenize("(+\n4 2)"), ["(", "+", "4", "2", ")"])

    def test_lexer_tabs(self):
        self.assertEqual(self.lexer.tokenize("(+\t4 2)"), ["(", "+", "4", "2", ")"])

if __name__ == "__main__":
    unittest.main()
