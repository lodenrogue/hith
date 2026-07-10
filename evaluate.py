import os
import re
import random
from lexer import Lexer
from parser import Parser
from htypes import NIL, Atom, T, Integer, Float, String, Symbol


LIBS_DIR = os.path.dirname(os.path.abspath(__file__)) + "/libs"


class Evaluator:

    def __init__(self):
        self.lexer = Lexer()
        self.parser = Parser()
        self.global_env = Env(Variables(), BuiltInFunctions(), MacroScope(), parent=None)
        self.load_libs()


    def load_libs(self):
        for filename in os.listdir(LIBS_DIR):
            path = os.path.join(LIBS_DIR, filename)

            if os.path.isfile(path):
                with open(path, "r") as f:
                    script = f.read()
                    self.evaluate(script)


    def evaluate(self, exp):
        ast = self.parser.build_ast(self.lexer.tokenize(exp))

        result = NIL
        for node in ast:
            result = self.evaluate_node(node, self.global_env)

        return result


    def evaluate_node(self, node, env):
        if self.is_nil(node):
            return node

        if self.is_atom(node):
            if self.is_symbol(node):
                return env.symbol_value(node)
            else:
                return node

        if isinstance(node, list) and len(node) == 0:
            return NIL

        raw_head, *raw_args = node
        head = self.evaluate_node(raw_head, env) if isinstance(raw_head, list) else raw_head

        if self.is_special_form(head):
            return self.handle_special_form(head, raw_args, env)

        macro = env.macro(head)
        if macro is not None:
            expansion = macro(*raw_args)
            return self.evaluate_node(expansion, env)

        return self.funcall(head, raw_args, env)
    

    def handle_special_form(self, head, tail, env):
        head = head.value

        if head == "quote":
            return self.quote(tail[0])

        if head == "backquote":
            return self.backquote(tail[0], env)

        if head == "defvar":
            return self.defvar(name=tail[0], value=tail[1], env=env)

        if head == "setq":
            return self.setq(name=tail[0], value=tail[1], env=env)

        if head == "symbol-value":
            return self.symbol_value(*tail, env)

        if head == "if":
            cond = tail[0]
            dothen = tail[1]
            doelse = tail[2] if len(tail) == 3 else None
            return self.doif(cond, dothen, doelse, env=env)

        if head == "defun":
            return self.defun(name=tail[0], params=tail[1], body=tail[2:], env=env)

        if head == "defmacro":
            return self.defmacro(name=tail[0], params=tail[1], body=tail[2:], env=env)

        if head == "format":
            return self.doformat(body=tail, env=env)

        if head == "message":
            return self.message(body=tail, env=env)

        if head == "length":
            return self.length(*tail, env=env)

        if head == "progn":
            return self.progn(*tail, env=env)

        if head == "funcall":
            return self.funcall(fn=tail[0], args=tail[1:], env=env)


    def is_quoted(self, node):
        return isinstance(node, str) and node.startswith("'")

        
    def is_special_form(self, symbol):
        return symbol.value in [
            "quote",
            "backquote",
            "defvar",
            "setq",
            "symbol-value",
            "if",
            "defun",
            "defmacro",
            "format",
            "message",
            "length",
            "progn",
            "funcall"
        ]


    def is_nil(self, node):
        return node == NIL


    def is_atom(self, node):
        return self.global_env.functions.data["atom?"](node) == T


    def is_symbol(self, node):
        return self.global_env.functions.data["symbol?"](node) == T


    def is_integer(self, node):
        return self.global_env.functions.data["int?"](node) == T


    def is_float(self, node):
        return self.global_env.functions.data["float?"](node) == T


    def is_string(self, node):
        return self.global_env.functions.data["string?"](node) == T


    def quote(self, arg):
        return arg


    def backquote(self, template, env):
        return self._expand_backquote(template, env)


    def _expand_backquote(self, node, env):
        if isinstance(node, list) and len(node) == 2 and isinstance(node[0], Symbol):
            operator = node[0].value

            if operator in ("unquote", "unquote-splice"):
                return self.evaluate_node(node[1], env)

        if isinstance(node, list):
            return self._expand_backquote_list(node, env)

        return node


    def _expand_backquote_list(self, items, env):
        result = []
        for item in items:
            if isinstance(item, list) and len(item) == 2 and isinstance(item[0], Symbol):
                operator, expr = item[0].value, item[1]

                if operator == "unquote-splice":
                    spliced = self.evaluate_node(expr, env)

                    if not isinstance(spliced, list):
                        raise TypeError(",@ (unquote-splice) requires a list result")

                    result.extend(spliced)
                    continue

                if operator == "unquote":
                    result.append(self.evaluate_node(expr, env))
                    continue

            if isinstance(item, list):
                result.append(self._expand_backquote_list(item, env))
            else:
                result.append(item)

        return result


    def defvar(self, name, value, env):
        env.variables.data[name.value] = self.evaluate_node(value, env)
        return name


    def setq(self, name, value, env):
        val = self.evaluate_node(value, env)

        if not env.set_symbol(name.value, val):
            env.variables.data[name.value] = val

        return name


    def symbol_value(self, tail, env):
        return env.symbol_value(self.evaluate_node(tail, env))


    def doif(self, cond, dothen, doelse, env):
        cond_value = self.evaluate_node(cond, env)

        if cond_value != NIL:
            return self.evaluate_node(dothen, env)
        else:
            if doelse:
                return self.evaluate_node(doelse, env)
            else:
                return NIL


    def defun(self, name, params, body, env):
        env.functions.data[name.value] = Function(self, params, body, env)
        return name


    def defmacro(self, name, params, body, env):
        env.macros.data[name.value] = Macro(self, params, body, env)
        return name

    def doformat(self, body, env):
        first = body[0]
        if isinstance(first, String):
            string = first
        else:
            string = self.evaluate_node(first, env)

        if len(body) == 1:
            return string

        formatted = string.value
        for arg in body[1:]:
            value = self.evaluate_node(arg, env)

            if value == T:
                value = "t"
            else:
                value = value.value

            if isinstance(value, str):
                value = strip_quotes(value)

            formatted = formatted.replace("%s", str(value), 1)

        result = String(formatted)
        return result


    def message(self, body, env):
        result = self.doformat(body, env)
        print(strip_quotes(result.value))
        return result


    def length(self, *args, env):
        sequence = self.evaluate_node(args[0], env)

        if isinstance(sequence, list):
            return Integer(len(sequence))

        return Integer(len(sequence.value) - 2)


    def progn(self, *args, env):
        result = NIL

        for arg in args:
            result = self.evaluate_node(arg, env)

        return result


    def funcall(self, fn, args, env):
        resolved = env.symbol_value(fn)
        fn_symbol = fn if self.is_nil(resolved) else resolved
        
        function = env.function(fn_symbol)
        if function is None:
            raise UndefinedFunctionException(f'Function with name {fn_symbol.value} is undefined')

        evaluated_args = [self.evaluate_node(arg, env) for arg in args]
        return function(*evaluated_args)


class Variables:

    def __init__(self):
        self.data = {}


class FunctionScope:

    def __init__(self):
        self.data = {}


class MacroScope:

    def __init__(self):
        self.data = {}


class BuiltInFunctions(FunctionScope):

    def __init__(self):
        self.data = self.__create_init_values()


    def __create_init_values(self):
        return {
            "make-symbol": lambda name: Symbol(strip_quotes(name.value)),
            "atom?": lambda e: self.cast_boolean(isinstance(e, Atom)),
            "int?": lambda e: self.cast_boolean(isinstance(e, Integer)),
            "float?": lambda e: self.cast_boolean(isinstance(e, Float)),
            "string?": lambda e: self.cast_boolean(isinstance(e, String)),
            "symbol?": lambda e: self.cast_boolean(isinstance(e, Symbol)),
            "+": lambda x, y: self.cast_arithmetic(x, y, x.value + y.value),
            "-": lambda x, y: self.cast_arithmetic(x, y, x.value - y.value),
            "*": lambda x, y: self.cast_arithmetic(x, y, x.value * y.value),
            "/": lambda x, y: self.cast_arithmetic(x, y, x.value / y.value),
            ">": lambda x, y: self.cast_boolean(x.value > y.value),
            "<": lambda x, y: self.cast_boolean(x.value < y.value),
            ">=": lambda x, y: self.cast_boolean(x.value >= y.value),
            "<=": lambda x, y: self.cast_boolean(x.value <= y.value),
            "eq": lambda x, y: self.cast_boolean(x.value == y.value),
            "nth": self.nth,
            "exit": lambda: exit(),
            "random": lambda: Float(random.random()),
            "round": lambda x: Integer(round(x.value)),
            "file-read-lines": self.file_read_lines,
            "list": lambda *args: list(args),
            "cons": self.cons,
            "car": lambda items: items[0] if items else NIL,
            "cdr": lambda items: items[1:] if items else [],
            "string-match": self.string_match,
            "string-to-number": self.string_to_number,
            "char-to-ord": self.char_to_ord,
            "ord-to-char": self.ord_to_char,
        }


    def ord_to_char(self, num):
        return String(f'"{chr(num.value)}"')


    def char_to_ord(self, char):
        stripped = strip_quotes(char.value)
        c = stripped[0]
        o = ord(c)
        return Integer(o)


    def string_to_number(self, string):
        value = strip_quotes(string.value)
        try:
            return Integer(int(value))
        except ValueError:
            try:
                return Float(float(value))
            except ValueError:
                return NIL


    def string_match(self, string, regex):
        pattern = re.compile(strip_quotes(regex.value))
        m = pattern.search(strip_quotes(string.value))
        if m:
            return Integer(m.start())
        else:
            return NIL


    def cast_arithmetic(self, x, y, result):
        if isinstance(x, Float) or isinstance(y, Float):
            return Float(result)

        return Integer(result)


    def cast_boolean(self, result):
        if result == True:
            return T
        else:
            return NIL


    def nth(self, index, items):
        index = index.value

        if isinstance(items, String):
            items = strip_quotes(items.value)

        if len(items) > index:
            value = items[index]

            if isinstance(value, str):
                return String(f'"{value}"')
            else:
                return value

        return NIL

    def cons(self, item, items):
        return [item] + list(items)

    def file_read_lines(self, path):
        path = path.value
        # remove the surrounding quotes
        path = path[1:-1]
        with open(path, "r") as f:
            return [String(line) for line in f.read().splitlines()]


class Env:

    def __init__(self, variables, functions, macros, parent):
        self.variables = variables
        self.functions = functions
        self.macros = macros
        self.parent = parent

    def set_symbol(self, name, value):
        if name in self.variables.data:
            self.variables.data[name] = value
            return True

        elif self.parent:
            return self.parent.set_symbol(name, value)

        else:
            return False

    def symbol_value(self, symbol):
        if symbol.value in self.variables.data:
            return self.variables.data[symbol.value]
        elif self.parent:
            return self.parent.symbol_value(symbol)
        else:
            return NIL

    def function(self, symbol):
        if symbol.value in self.functions.data:
            return self.functions.data[symbol.value]
        elif self.parent:
            return self.parent.function(symbol)
        else:
            return None

    def macro(self, symbol):
        if symbol.value in self.macros.data:
            return self.macros.data[symbol.value]
        elif self.parent:
            return self.parent.macro(symbol)
        else:
            return None


class ParamSpec:
    """Parses a lambda-list that may contain &rest, binding fixed params
    positionally and the remainder (as a Python list) to the rest param."""

    def __init__(self, params):
        self.fixed = []
        self.rest_name = None

        i = 0
        while i < len(params):
            p = params[i]
            if p.value == "&rest":
                self.rest_name = params[i + 1].value
                i += 2
            else:
                self.fixed.append(p.value)
                i += 1

    def bind(self, args):
        bound = dict(zip(self.fixed, args))
        if self.rest_name is not None:
            bound[self.rest_name] = list(args[len(self.fixed):])
        return bound


class Function:

    def __init__(self, evaluator, params, body, env):
        self.evaluator = evaluator
        self.param_spec = ParamSpec(params)
        self.body = body
        self.env = env

    def __call__(self, *args):
        variables = Variables()
        variables.data.update(self.param_spec.bind(list(args)))

        local_env = Env(variables, FunctionScope(), MacroScope(), parent=self.env)
        result = NIL

        for expression in self.body:
            result = self.evaluator.evaluate_node(expression, local_env)

        return result


class Macro:
    """Like Function, but receives raw (unevaluated) argument nodes and
    returns an expansion tree instead of a final value. &rest in the macro's
    param list collects the remaining raw argument nodes as a Python list,
    which is what `,@body` splices."""

    def __init__(self, evaluator, params, body, env):
        self.evaluator = evaluator
        self.param_spec = ParamSpec(params)
        self.body = body
        self.env = env

    def __call__(self, *raw_args):
        variables = Variables()
        variables.data.update(self.param_spec.bind(list(raw_args)))

        local_env = Env(variables, FunctionScope(), MacroScope(), parent=self.env)
        result = NIL

        for expression in self.body:
            result = self.evaluator.evaluate_node(expression, local_env)

        return result


class UndefinedFunctionException(Exception):
    """Raised when trying to access an undefined function"""
    pass


def strip_quotes(value):
    if isinstance(value, str) and len(value) >= 2 and value.startswith("\"") and value.endswith("\""):
        return value[1:-1]
    return value
