import unittest
from lexer import Lexer
from parser import Parser
from htypes import Atom, Integer, Float, String, Symbol


PRIMITIVE_EXAMPLE = "42"
SIMPLE_EXAMPLE = "(+ 1 2.3)"
COMPLEX_EXAMPLE = "(if (> x (+ 1.33 5.7)) (* x 2) 0)"
SPACES_EXAMPLE = "(defvar x \"hello() 33.23 world\")"

class TestParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.lexer = Lexer()
        cls.parser = Parser()

    def test_parser_ast_primitive(self):
        self.assertEqual(
            self.parser.build_ast(self.lexer.tokenize(PRIMITIVE_EXAMPLE)),
            [Integer(42)])

    def test_parser_ast_string(self):
        self.assertEqual(
            self.parser.build_ast(self.lexer.tokenize("\"Hello World () 33.43\"")),
            [String("\"Hello World () 33.43\"")])
        
    def test_parser_ast_simple(self):
        self.assertEqual(
            self.parser.build_ast(self.lexer.tokenize(SIMPLE_EXAMPLE)),
            [[Symbol("+"), Integer(1), Float(2.3)]])

    def test_parser_ast_complex(self):
        self.assertEqual(
            self.parser.build_ast(self.lexer.tokenize(COMPLEX_EXAMPLE)), 
            [[Symbol("if"),
              [Symbol(">"), Symbol("x"),
               [Symbol("+"), Float(1.33), Float(5.7)]],
              [Symbol("*"), Symbol("x"), Integer(2)],
              Integer(0)]]
        )

    def test_parser_ast_example_with_spaces(self):
        self.assertEqual(
            self.parser.build_ast(self.lexer.tokenize(SPACES_EXAMPLE)),
            [[Symbol("defvar"), Symbol("x"), String("\"hello() 33.23 world\"")]])
        

if __name__ == "__main__":
    unittest.main()
