from lexer import Lexer
from parser import Parser


class Evaluator:

    def __init__(self):
        #self.env = env
        self.lexer = Lexer()
        self.parser = Parser()

        self.functions = {
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "*": lambda x, y: x * y,
            "/": lambda x, y: x / y,
            ">": lambda x, y: x > y,
            "<": lambda x, y: x < y,
            ">=": lambda x, y: x >= y,
            "<=": lambda x, y: x <= y,
            "eq": lambda x, y: x == y,
            "if": lambda cond, dothen, doelse: self.doif(cond, dothen, doelse),
            "symbol-value": self.symbol_value,
            "defvar": self.defvar
        }


    def evaluate(self, exp):
        ast = self.parser.build_ast(self.lexer.tokenize(exp))
        
        if isinstance(ast, list):
            return self.evaluate_node(ast)
        
        if self.is_number(ast):
            return ast
        
        value = self.symbol_value(ast)
        return ast if value is None else value


    def evaluate_node(self, node):
        if self.should_not_evaluate(node):
            return node
        
        if isinstance(node, list):
            head = self.evaluate_node(node[0]) if isinstance(node[0], list) else node[0]
            
            if self.is_special_form(head):
                tail = node[1:]
            else:
                tail = [self.evaluate_node(n) for n in node[1:]]
                
            function = self.functions[head]
            return function(*tail)
        else:
            if self.is_string(node) or self.is_number(node):
                return node
            else:
                return self.symbol_value(node)


    def should_not_evaluate(self, node):
        return isinstance(node, str) and node.startswith("'")

        
    def is_special_form(self, symbol):
        return symbol in ["defvar", "if"]


    def is_string(self, x):
        return isinstance(x, str) and len(x) > 0 and x.startswith("\"")


    def is_number(self, x):
        return isinstance(x, (int, float))


    def doif(self, cond, dothen, doelse):
        cond_value = self.evaluate_node(cond)
        
        if cond_value is not False and cond_value != "False":
            return self.evaluate_node(dothen)
        else:
            return self.evaluate_node(doelse)


    def symbol_value(self, x):
        if x.startswith("'"):
            x = x[1:]

        if x in variables.data:
            return variables.data[x]
        else:
            return None


    def defvar(self, name, value):
        variables.data[name] = value
        return name


class Variables():
    def __init__(self):
        self.data = self.__create_init_values()

    def __create_init_values(self):
        return {
            "False": False
        }

    def clear(self):
        self.data = self.__create_init_values()


variables = Variables()
