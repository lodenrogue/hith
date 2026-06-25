class Lexer:

    def tokenize(self, string):
        tokens = []
        collector = ""
        in_string = False

        for c in string:
            if c in "() " and not in_string:
                if collector != "":
                    tokens.append(collector)
                    collector = ""

                if c != " ":
                    tokens.append(c)

            elif c == "\"":
                collector += c
                in_string = not in_string

            else:
                collector += c

        if collector != "":
            tokens.append(collector)

        return tokens
