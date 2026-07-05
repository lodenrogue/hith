class Atom:

    def __init__(self, value):
        self.value = value


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
