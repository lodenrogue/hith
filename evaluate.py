from lexer import Lexer
from parser import Parser
from htypes import Atom, Boolean, Integer, Float, String, Symbol


class Evaluator:

    def __init__(self):
        self.lexer = Lexer()
        self.parser = Parser()
        self.global_env = Env(Variables(), BuiltInFunctions(), parent=None)


    def evaluate(self, exp):
        ast = self.parser.build_ast(self.lexer.tokenize(exp))

        for node in ast:
            result = self.evaluate_node(node, self.global_env)

        return result


    def evaluate_node(self, node, env):
        if self.is_atom(node):
            if self.is_symbol(node):
                return env.symbol_value(node)
            else:
                return node

        raw_head, *raw_args = node
        head = self.evaluate_node(raw_head, env).value if isinstance(raw_head, list) else raw_head.value

        if self.is_special_form(head):
            return self.handle_special_form(head, raw_args, env)

        function = env.function(head)
        if function == None:
            raise UndefinedFunctionException(f'Function with name {head} is undefined')

        evaluated_args = [self.evaluate_node(n, env) for n in raw_args]
        return function(*evaluated_args)
    

    def handle_special_form(self, head, tail, env):
        if head == "quote":
            return self.quote(tail[0])

        if head == "defvar" or head == "setq":
            return self.defvar(name=tail[0], value=tail[1], env=env)

        if head == "symbol-value":
            return self.symbol_value(*tail, env)

        if head == "if":
            return self.doif(*tail, env)

        if head == "defun":
            return self.defun(name=tail[0], params=tail[1], body=tail[2:], env=env)

        if head == "message":
            return self.message(*tail, env)

        if head == "length":
            return self.length(*tail, env=env)

        if head == "progn":
            return self.progn(*tail, env=env)

        if head == "while":
            return self.dowhile(condition=tail[0], body=tail[1:], env=env)


    def is_quoted(self, node):
        return isinstance(node, str) and node.startswith("'")

        
    def is_special_form(self, symbol):
        return symbol in [
            "quote",
            "defvar",
            "setq",
            "symbol-value",
            "if",
            "defun",
            "message",
            "length",
            "progn",
            "while"
        ]


    def is_atom(self, node):
        return self.global_env.functions.data["atom"](node)


    def is_symbol(self, node):
        return self.global_env.functions.data["symbolp"](node)


    def is_integer(self, node):
        return self.global_env.functions.data["intp"](node)


    def is_float(self, node):
        return self.global_env.functions.data["floatp"](node)


    def is_string(self, node):
        return self.global_env.functions.data["stringp"](node)


    def quote(self, arg):
        return arg


    def defvar(self, name, value, env):
        env.variables.data[name.value] = self.evaluate_node(value, env)
        return name


    def symbol_value(self, tail, env):
        return env.symbol_value(self.evaluate_node(tail, env))


    def doif(self, cond, dothen, doelse, env):
        cond_value = self.evaluate_node(cond, env)
        
        if cond_value is not False and cond_value != "False":
            return self.evaluate_node(dothen, env)
        else:
            return self.evaluate_node(doelse, env)


    def defun(self, name, params, body, env):
        env.functions.data[name] = Function(self, params, body, env)
        return name


    def message(self, body, env):
        string = self.evaluate_node(body, env)
        print(string)
        return string


    def length(self, *args, env):
        value = self.evaluate_node(args[0], env)

        if isinstance(value, list):
            return len(value)

        return len(value) - 2


    def progn(self, *args, env):
        result = None

        for arg in args:
            result = self.evaluate_node(arg, env)

        return result


    def dowhile(self, condition, body, env):
        while self.evaluate_node(condition, env):
            for expression in body:
                self.evaluate_node(expression, env)


class Variables:
    def __init__(self):
        self.data = self.__create_init_values()


    def __create_init_values(self):
        return {
            "False": False
        }


class FunctionScope:

    def __init__(self):
        self.data = {}
        

class BuiltInFunctions(FunctionScope):

    def __init__(self):
        self.data = self.__create_init_values()


    def __create_init_values(self):
        return {
            "atom": lambda e: isinstance(e, Atom),
            "intp": lambda e: isinstance(e, Integer),
            "floatp": lambda e: isinstance(e, Float),
            "stringp": lambda e: isinstance(e, String),
            "symbolp": lambda e: isinstance(e, Symbol),
            "+": lambda x, y: Float(x.value + y.value),
            "-": lambda x, y: Float(x.value - y.value),
            "*": lambda x, y: Float(x.value * y.value),
            "/": lambda x, y: Float(x.value / y.value),
            ">": lambda x, y: Boolean(x.value > y.value),
            "<": lambda x, y: Boolean(x.value < y.value),
            ">=": lambda x, y: Boolean(x.value >= y.value),
            "<=": lambda x, y: Boolean(x.value <= y.value),
            "eq": lambda x, y: Boolean(x.value == y.value),
            "nth": self.nth,
            "exit": lambda: exit(),
            "file-read-lines": self.file_read_lines
        }


    def nth(self, index, items):
        if len(items) > index:
            return items[index]

        return None

    def file_read_lines(self, path):
        # remove the surrounding quotes
        path = path[1:-1]
        with open(path, "r") as f:
            return f.read().splitlines()


class Env:

    def __init__(self, variables, functions, parent):
        self.variables = variables
        self.functions = functions
        self.parent = parent

    def symbol_value(self, symbol):
        if symbol.value in self.variables.data:
            return self.variables.data[symbol.value]
        elif self.parent:
            return self.parent.symbol_value(symbol)
        else:
            return None

    def function(self, symbol):
        if symbol in self.functions.data:
            return self.functions.data[symbol]
        elif self.parent:
            return self.parent.function(symbol)
        else:
            return None


class Function:

    def __init__(self, evaluator, params, body, env):
        self.evaluator = evaluator
        self.params = params
        self.body = body
        self.env = env

    def __call__(self, *args):
        variables = Variables()
        variables.data.update(zip(self.params, args))

        local_env = Env(variables, FunctionScope(), parent=self.env)
        result = None

        for expression in self.body:
            result = self.evaluator.evaluate_node(expression, local_env)

        return result
    

class UndefinedFunctionException(Exception):
    """Raised when trying to access an undefined function"""
    pass
