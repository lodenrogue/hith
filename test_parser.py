import unittest
from lexer import Lexer
from parser import Parser

PRIMITIVE_EXAMPLE = "42"
SIMPLE_EXAMPLE = "(+ 1 2.3)"
COMPLEX_EXAMPLE = "(if (> x (+ 1.33 5.7)) (* x 2) 0)"
SPACES_EXAMPLE = "(defvar x \"hello() 33.23 world\")"

class TestInterpreter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.lexer = Lexer()
        cls.parser = Parser()

    def test_parser_ast_primitive(self):
        self.assertEqual(
            self.parser.build_ast(self.lexer.tokenize(PRIMITIVE_EXAMPLE)),
            42)

    def test_parser_ast_string(self):
        self.assertEqual(
            self.parser.build_ast(self.lexer.tokenize("\"Hello World () 33.43\"")),
            "\"Hello World () 33.43\"")
        
    def test_parser_ast_simple(self):
        self.assertEqual(
            self.parser.build_ast(self.lexer.tokenize(SIMPLE_EXAMPLE)),
            ["+", 1, 2.3])

    def test_parser_ast_complex(self):
        self.assertEqual(
            self.parser.build_ast(self.lexer.tokenize(COMPLEX_EXAMPLE)), 
            ["if", [">", "x", ["+", 1.33, 5.7]], ["*", "x", 2], 0]
        )

    def test_parser_ast_example_with_spaces(self):
        self.assertEqual(
            self.parser.build_ast(self.lexer.tokenize(SPACES_EXAMPLE)),
            ["defvar", "x", "\"hello() 33.23 world\""])
        
if __name__ == "__main__":
    unittest.main()
