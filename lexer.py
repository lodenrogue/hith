class Lexer:

    def tokenize(self, string):
        tokens = []
        collector = ""
        in_string = False
        i = 0
        n = len(string)

        while i < n:
            c = string[i]

            if in_string:
                collector += c
                if c == "\"":
                    in_string = False
                i += 1
                continue

            if c == "\"":
                collector += c
                in_string = True
                i += 1
                continue

            if c in "()" or c.isspace():
                if collector != "":
                    tokens.append(collector)
                    collector = ""
                if not c.isspace():
                    tokens.append(c)
                i += 1
                continue

            if c == "`":
                if collector != "":
                    tokens.append(collector)
                    collector = ""
                tokens.append("`")
                i += 1
                continue

            if c == "'":
                if collector != "":
                    tokens.append(collector)
                    collector = ""
                tokens.append("'")
                i += 1
                continue

            if c == ",":
                if collector != "":
                    tokens.append(collector)
                    collector = ""
                if i + 1 < n and string[i + 1] == "@":
                    tokens.append(",@")
                    i += 2
                else:
                    tokens.append(",")
                    i += 1
                continue

            collector += c
            i += 1

        if collector != "":
            tokens.append(collector)

        return tokens
