# parser.py

import json
from htypes import Atom, Boolean, Integer, Float, String, Symbol


class Parser:

    def build_ast(self, tokens):
        tree = Node([])
        current_node = tree
        pending_wrappers = []  # stack of "quote"/"backquote"/"unquote"/"unquote-splice"
                                # waiting to wrap the *next* complete form

        i = 0
        while i < len(tokens):
            raw_token = tokens[i]

            if raw_token == "'":
                pending_wrappers.append("quote")
                i += 1
                continue

            if raw_token == "`":
                pending_wrappers.append("backquote")
                i += 1
                continue

            if raw_token == ",@":
                pending_wrappers.append("unquote-splice")
                i += 1
                continue

            if raw_token == ",":
                pending_wrappers.append("unquote")
                i += 1
                continue

            token = self.atomize(raw_token)

            if token == "(":
                new_node = Node([])
                new_node.wrappers = list(pending_wrappers)
                pending_wrappers = []
                current_node.data.append(new_node)
                new_node.parent = current_node
                current_node = new_node
            elif token == ")":
                current_node = current_node.parent
            else:
                wrapped = token
                for w in reversed(pending_wrappers):
                    wrapped = Node([Symbol(w), wrapped])
                pending_wrappers = []
                current_node.data.append(wrapped)

            i += 1

        return self.unwrap_node(tree)

    
    def atomize(self, token):
        if token in ("(", ")"):
            return token

        try:
            return Integer(int(token))
        except ValueError:
            try:
                return Float(float(token))
            except ValueError:
                if token == "True":
                    return Boolean(True)

                if token == "False":
                    return Boolean(False)

                if self.is_string(token):
                     return String(token)
                 
                return Symbol(token)


    def is_string(self, token):
       return token.startswith("\"") and token.endswith("\"")
   

    def unwrap_node(self, node):
        unwrapped = []

        for token in node.data:
            if isinstance(token, Node):
                inner = self.unwrap_node(token)
                wrappers = getattr(token, "wrappers", [])
                for w in reversed(wrappers):
                    inner = [Symbol(w), inner]
                unwrapped.append(inner)
            else:
                unwrapped.append(token)

        return unwrapped


class Node:

    def __init__(self, data):
        self.data = data
        self.parent = None
        self.wrappers = []
