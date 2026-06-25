from lexer import Lexer
from parser import Parser


lexer = Lexer()
parser = Parser()


def evaluate(exp):
    ast = parser.build_ast(lexer.tokenize(exp))

    if isinstance(ast, list):
        return __evaluate_node(ast)

    if is_number(ast):
        return ast

    value = symbol_value(ast)
    return ast if value is None else value

        

def __evaluate_node(node):
    if __should_not_evaluate(node):
        return node

    if isinstance(node, list):
        head = __evaluate_node(node[0]) if isinstance(node[0], list) else node[0]

        if __is_special_form(head):
            tail = node[1:]
        else:
            tail = [__evaluate_node(n) for n in node[1:]]

        function = functions[head]
        return function(*tail)
    else:
        if is_string(node) or is_number(node):
            return node
        else:
            return symbol_value(node)


def __should_not_evaluate(node):
    return isinstance(node, str) and node.startswith("'")

        
def __is_special_form(symbol):
    return symbol in ["defvar"]


def is_string(x):
    return isinstance(x, str) and len(x) > 0 and x.startswith("\"")


def is_number(x):
    return isinstance(x, (int, float))


def symbol_value(x):
    if x.startswith("'"):
        x = x[1:]

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

