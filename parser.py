import json
from htypes import Atom, Integer, Float, String

class Parser:

    def build_ast(self, tokens):
        tree = Node([])
        current_node = tree

        for raw_token in tokens:
            token = self.atomize(raw_token)

            if token == "(":
                new_node = Node([])
                current_node.data.append(new_node)
                new_node.parent = current_node
                current_node = new_node
            elif token == ")":
                current_node = current_node.parent
            else:
                current_node.data.append(token)

        return self.unwrap_node(tree)

    
    def atomize(self, token):
        try:
            return Integer(int(token))
        except ValueError:
            try:
                return Float(float(token))
            except ValueError:
                 if self.is_string(token):
                     return String(token)
                 return token


    def is_string(self, token):
       return token.startswith("\"") and token.endswith("\"")
            

    def unwrap_node(self, node):
        unwrapped = []

        for token in node.data:
            if isinstance(token, Node):
                unwrapped.append(self.unwrap_node(token))
            else:
                unwrapped.append(token)

        return unwrapped


class Node:

    def __init__(self, data):
        self.data = data
        self.parent = None
