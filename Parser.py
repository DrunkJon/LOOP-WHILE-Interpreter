from Tokenizer import Tokenizer, Token
from Nodes import*


class Parser:
    tokenizer: Tokenizer
    token_stream: iter
    cur_token: Token
    context = {
        "VAR": {},
        "NAME": {}
    }

    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer

    def _next(self):
        # throws StopIteration if no tokens are left
        while True:
            self.cur_token = next(self.token_stream)
            if self.cur_token.type != "WHITESPACE":
                break

    def eat(self, types, endpoint=False) -> Token:
        if not isinstance(types, list):
            types = [types]
        got = "eat error"
        try:
            self._next()
            assert self.cur_token.type in types
            return self.cur_token
        except StopIteration:
            if endpoint:
                raise EndOfTokenStreamError()
            else:
                got = "end of token stream"
                raise SyntaxError(f"expected {' '.join(f'{t} or' for t in types)[:-3]} got {got}")
        except AssertionError:
            got = self.cur_token.type
            raise SyntaxError(f"expected {' '.join(f'{t} or' for t in types)[:-3]} got {got}")

    def parse(self, txt: str):
        self.token_stream = self.tokenizer.tokenize(txt)
        operations = []
        while True:
            try:
                operations.append(self.parse_operation())
            except EndOfTokenStreamError:
                break
        context = self.context
        for node in operations:
            node.eval(context)
        print(context["VAR"])
        self.context = context

    def parse_operation(self):
        token = self.eat(["LOOP", "WHILE", "NAME", "END", "VAR"], endpoint=True)
        # Blocks
        if token.type == "NAME":
            name = token.value
            inputs = []
            while True:
                token = self.eat(["PARAM", "BEGIN"])
                if token.type == "BEGIN":
                    break
                else:
                    if token.value in inputs:
                        raise SyntaxError(f"{name} already has input {'n' + str(token.value)}")
                    else:
                        inputs.append(token.value)
            inner = []
            while True:
                node = self.parse_operation()
                if node:
                    inner.append(node)
                else:
                    break
            return NameDefNode(name, inner, inputs)

        elif token.type == "LOOP":
            counter = VarNode(self.eat("VAR").value)
            self.eat("BEGIN")
            inner = []
            while True:
                node = self.parse_operation()
                if node:
                    inner.append(node)
                else:
                    break
            return LoopNode(counter, inner)

        elif token.type == "WHILE":
            counter = VarNode(self.eat("VAR").value)
            self.eat("NOT_ZERO")
            self.eat("BEGIN")
            inner = []
            while True:
                node = self.parse_operation()
                if node:
                    inner.append(node)
                else:
                    break
            return WhileNode(counter, inner)

        # Block End
        elif token.type == "END":
            return None

        # Assign
        elif token.type == "VAR":
            var = VarNode(token.value)
            self.eat("ASSIGN")
            right = self.parse_term()
            return AssignNode(var, right)

    def parse_term(self):
        token = self.eat(["VAR", "NAME"])
        if token.type == "VAR":
            var = VarNode(token.value)
            operator = self.eat(["PLUS", "MINUS"])
            const = ConstNode(self.eat("CONST").value)
            if operator.type == "PLUS":
                return PlusNode(var, const)
            elif operator.type == "MINUS":
                return MinusNode(var, const)
        if token.type == "NAME":
            name = token.value
            inputs = []
            while True:
                token = self.eat(["VAR", "END"])
                if token.type == "END":
                    break
                else:
                    inputs.append(VarNode(token.value))
            return NameCallNode(name, inputs)


# Custom Error
class EndOfTokenStreamError(Exception):
    pass
