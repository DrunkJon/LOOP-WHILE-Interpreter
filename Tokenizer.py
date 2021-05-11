import re


class Token:
    type: str
    value: any

    def __init__(self, token_type: str, value: str = None):
        self.type = token_type
        self.value = value

    def __repr__(self):
        return f'[{self.type}: {self.value}]'


class Tokenizer:
    def __init__(self, grammar: dict):
        """
        :param grammar: {TOKENNAME: (REGEX-PATTERN, VALUE-FUNCTION or None), ...}
        """
        self.grammar = grammar

    def tokenize(self, input_text: str):
        """
        :param input_text: text to be interpreted with this grammar
        :yield: Tokens
        """
        # building errors-case
        def raise_unmatched(val):
            raise SyntaxError(f'"{val}" cannot be tokenized')
        self.grammar['UNMATCHED'] = (r'.+', raise_unmatched)

        grammar_regex = '|'.join(f'(?P<{name}>{tup[0]})' for name, tup in self.grammar.items())

        for match_object in re.finditer(grammar_regex, input_text):
            token_type = match_object.lastgroup
            value = match_object.group()
            if self.grammar[token_type][1]:
                value = self.grammar[token_type][1](value)
            yield Token(token_type, value)

