from lexer import Lexer
from parser import Parser


lexer = Lexer()
parser = Parser()


def evaluate(exp):
    ast = parser.build_ast(lexer.tokenize(exp))
    return __evaluate_node(ast)

def __evaluate_node(node):
    if isinstance(node, list):
        if isinstance(node[0], list):
            head = __evaluate_node(node[0])
        else:
            head = node[0]

        function = env[head]
        tail = [__evaluate_node(n) for n in node[1:]]
        return function(*tail)
    else:
        return node


env = {
    "+": lambda x, y: x + y
}

