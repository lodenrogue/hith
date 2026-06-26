from lexer import Lexer
from parser import Parser


lexer = Lexer()
parser = Parser()


def evaluate(exp):
    ast = parser.build_ast(lexer.tokenize(exp))

    if isinstance(ast, list):
        return evaluate_node(ast)

    if is_number(ast):
        return ast

    value = symbol_value(ast)
    return ast if value is None else value


def evaluate_node(node):
    if __should_not_evaluate(node):
        return node

    if isinstance(node, list):
        head = evaluate_node(node[0]) if isinstance(node[0], list) else node[0]

        if __is_special_form(head):
            tail = node[1:]
        else:
            tail = [evaluate_node(n) for n in node[1:]]

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
    return symbol in ["defvar", "if"]


def is_string(x):
    return isinstance(x, str) and len(x) > 0 and x.startswith("\"")


def is_number(x):
    return isinstance(x, (int, float))


def doif(cond, dothen, doelse):
    cond_value = evaluate_node(cond)

    if cond_value is not False and cond_value != "False":
        return evaluate_node(dothen)
    else:
        return evaluate_node(doelse)


def symbol_value(x):
    if x.startswith("'"):
        x = x[1:]

    if x in variables.data:
        return variables.data[x]
    else:
        return None


def defvar(name, value):
    variables.data[name] = value


class Variables(dict):
    def __init__(self):
        self.data = self.__create_init_values()

    def __create_init_values(self):
        return {
            "False": False
        }

    def clear(self):
        self.data = self.__create_init_values()


variables = Variables()

functions = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x / y,
    ">": lambda x, y: x > y,
    "<": lambda x, y: x < y,
    ">=": lambda x, y: x >= y,
    "<=": lambda x, y: x <= y,
    "eq": lambda x, y: x == y,
    "if": lambda cond, dothen, doelse: doif(cond, dothen, doelse),
    "symbol-value": symbol_value,
    "defvar": defvar
}
