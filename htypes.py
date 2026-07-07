class Nil:

    def __init__(self):
        self.value = "nil"

    def __eq__(self, other):
        return type(self) == type(other)

class Atom:

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return type(self) == type(other) and self.value == other.value


class Boolean(Atom):

    def __init__(self, value):
        super().__init__(value)


class Integer(Atom):

    def __init__(self, value):
        super().__init__(value)


class Float(Atom):

    def __init__(self, value):
        super().__init__(value)


class String(Atom):

    def __init__(self, value):
        super().__init__(value)


class Symbol(Atom):

    def __init__(self, value):
        super().__init__(value)
