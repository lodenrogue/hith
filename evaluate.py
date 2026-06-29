from lexer import Lexer
from parser import Parser


class Evaluator:

    def __init__(self):
        self.lexer = Lexer()
        self.parser = Parser()
        self.global_env = Env(Variables(), parent=None)

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
        }


    def evaluate(self, exp):
        ast = self.parser.build_ast(self.lexer.tokenize(exp))
        return self.evaluate_node(ast, self.global_env)


    def evaluate_node(self, node, env):
        if self.is_string(node) or self.is_number(node) or self.is_quoted(node):
            return node

        elif isinstance(node, list):
            head = self.evaluate_node(node[0], env) if isinstance(node[0], list) else node[0]
            
            if self.is_special_form(head):
                return self.handle_special_form(head, node[1:], env)
            else:
                tail = [self.evaluate_node(n, env) for n in node[1:]]
                function = self.functions[head]
                return function(*tail)
        else:
            return env.symbol_value(node)


    def handle_special_form(self, head, tail, env):
        if head == "defvar" or head == "setq":
            return self.defvar(*tail, env)
        if head == "symbol-value":
            return self.symbol_value(*tail, env)
        elif head == "if":
            return self.doif(*tail, env)


    def is_quoted(self, node):
        return isinstance(node, str) and node.startswith("'")

        
    def is_special_form(self, symbol):
        return symbol in ["defvar", "setq", "symbol-value", "if"]


    def is_string(self, x):
        return isinstance(x, str) and len(x) > 0 and x.startswith("\"")


    def is_number(self, x):
        return isinstance(x, (int, float))


    def defvar(self, name, value, env):
        env.variables.data[name] = self.evaluate_node(value, env)
        return name


    def symbol_value(self, tail, env):
        return env.symbol_value(self.evaluate_node(tail, env))


    def doif(self, cond, dothen, doelse, env):
        cond_value = self.evaluate_node(cond, env)
        
        if cond_value is not False and cond_value != "False":
            return self.evaluate_node(dothen, env)
        else:
            return self.evaluate_node(doelse, env)


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


    def clear_variables(self):
        self.variables.clear()
