from lexer import Lexer
from parser import Parser


class Evaluator:

    def __init__(self, env):
        self.env = env
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
            "symbol-value": self.env.symbol_value,
            "setq": self.env.defvar,
            "defvar": self.env.defvar
        }


    def evaluate(self, exp):
        ast = self.parser.build_ast(self.lexer.tokenize(exp))
        
        if isinstance(ast, list):
            return self.evaluate_node(ast)
        
        if self.is_number(ast):
            return ast
        
        value = self.env.symbol_value(ast)
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
                return self.env.symbol_value(node)


    def should_not_evaluate(self, node):
        return isinstance(node, str) and node.startswith("'")

        
    def is_special_form(self, symbol):
        return symbol in ["defvar", "setq", "if"]


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


class Variables():
    def __init__(self):
        self.data = self.__create_init_values()

    def __create_init_values(self):
        return {
            "False": False
        }

    def clear(self):
        self.data = self.__create_init_values()


class Env:

    def __init__(self, variables, parent):
        self.variables = variables
        self.parent = parent

    def symbol_value(self, symbol):
        if symbol.startswith("'"):
            symbol = symbol[1:]

        if symbol in self.variables.data:
            return self.variables.data[symbol]
        elif self.parent:
            return self.parent.symbol_value(symbol)
        else:
            return None

    def defvar(self, name, value):
        self.variables.data[name] = value
        return name

    def clear_variables(self):
        self.variables.clear()
