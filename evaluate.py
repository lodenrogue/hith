from lexer import Lexer
from parser import Parser


lexer = Lexer()
parser = Parser()


def evaluate(exp):
    ast = parser.build_ast(lexer.tokenize(exp))

    if isinstance(ast, list):
        return __evaluate_node(ast)
    else:
        value = symbol_value(ast)

        if value is None:
            return ast
        else:
            return value
        

def __evaluate_node(node):
    if isinstance(node, list):
        if isinstance(node[0], list):
            head = __evaluate_node(node[0])
        else:
            head = node[0]

        tail = [__evaluate_node(n) for n in node[1:]]
        function = functions[head]
        return function(*tail)
    else:
        return node


def symbol_value(x):
    if x in variables:
        return variables[x]
    else:
        return None


def defvar(name, value):
    variables[name] = value


variables = {}

functions = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x / y,
    "symbol-value": symbol_value,
    "defvar": defvar
}

