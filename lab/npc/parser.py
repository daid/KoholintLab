from .tokenizer import Token, Tokenizer, ParseError
from typing import Tuple, Dict, Callable, List, Optional


class AstNode:
    def __init__(self, kind: str, token: Token, *params: Optional["AstNode"]):
        self.kind = kind
        self.token = token
        self.params = params
    
    def get_identifier(self) -> str:
        if self.kind != "value" or self.token.kind != "ID":
            raise ParseError(self.token, f"Expected identifier, got {self} instead")
        return self.token.value

    def get_string(self) -> str:
        if self.kind != "value" or self.token.kind != "STRING":
            raise ParseError(self.token, f"Expected a string, got {self} instead")
        return self.token.value

    def get_number(self) -> int:
        if self.kind != "value" or self.token.kind != "NUMBER":
            raise ParseError(self.token, f"Expected a number, got {self} instead")
        return self.token.value

    def is_number(self):
        if self.kind != 'value':
            return False
        if self.token.kind != 'NUMBER':
            return False
        return True

    def is_string(self):
        if self.kind != 'value':
            return False
        if self.token.kind != 'STRING':
            return False
        return True
    
    def dump(self, indent=0):
        print("  " * indent, self.kind, self.token)
        for param in self.params:
            if isinstance(param, list):
                print("  " * indent, "  [")
                for p in param:
                    p.dump(indent+2)
                print("  " * indent, "  ]")
            else:
                param.dump(indent+1)

    def __repr__(self):
        if self.kind == 'value':
            if self.is_string():
                return repr(self.token.value)
            return f"{self.token.value}"
        params = ', '.join(("[...]" if isinstance(p, list) else repr(p)) for p in self.params)
        return f"{self.kind}({params})"



def parse_block(tok):
    block = []
    block_indent = tok.expect("NEWLINE").value
    while True:
        if tok.match("EOF"):
            break
        if token := tok.match("ID", "if"):
            condition = parse_expression(tok)
            tok.expect(":")
            if_block = parse_block(tok)
            block.append(AstNode("if", token, condition, if_block))
        elif token := tok.match("ID", "else"):
            tok.expect(":")
            if not block or block[-1].kind != "if" or len(block[-1].params) != 2:
                raise ParseError(token, f"Unexpected else")
            else_block = parse_block(tok)
            block[-1] = AstNode("if", block[-1].token, *block[-1].params, else_block)
        else:
            expression = parse_expression(tok)
            if token := tok.match("="): # Assignment
                expression = AstNode("=", token, expression, parse_expression(tok))
            block.append(expression)
        token = tok.peek()
        if token.kind == "EOF":
            break
        if token.kind != "NEWLINE":
            raise ParseError(token, f"Unexpected {token.value} ({token.kind}), expected a NEWLINE")
        if token.value > block_indent:
            raise ParseError(token, f"Unexpected indentation")
        if token.value < block_indent:
            break
        tok.pop()
    return block


PREC_NONE = 0
PREC_ASSIGNMENT = 1  # =
PREC_LOGIC_OR = 2  # or
PREC_LOGIC_AND = 3  # and
PREC_EQUALITY = 4  # == !=
PREC_COMPARISON = 5  # < > <= >=
PREC_TERM = 6  # + -
PREC_BITWISE_OR = 7  # |
PREC_BITWISE_XOR = 8  # ^
PREC_BITWISE_AND = 9  # &
PREC_SHIFT = 10  # << >>
PREC_FACTOR = 11  # * /
PREC_UNARY = 12  # ! -
PREC_CALL = 13  # . () []
PREC_PRIMARY = 14


def parse_value(tok: Tokenizer) -> AstNode:
    t = tok.pop()
    return AstNode("value", t)


def parse_grouping(tok: Tokenizer) -> AstNode:
    tok.pop()
    res = parse_precedence(tok, PREC_ASSIGNMENT)
    tok.expect(')')
    return res


def parse_call(tok: Tokenizer) -> AstNode:
    tok.expect('(')
    if tok.match(')'):
        return 'call', []
    args = [parse_precedence(tok, PREC_ASSIGNMENT)]
    while tok.match(','):
        args.append(parse_precedence(tok, PREC_ASSIGNMENT))
    tok.expect(')')
    return 'call', args


def parse_ref(tok: Tokenizer) -> AstNode:
    t = tok.pop()
    res = parse_precedence(tok, PREC_ASSIGNMENT)
    tok.expect(']')
    return AstNode('REF', t, res)


def parse_unary(tok: Tokenizer) -> AstNode:
    t = tok.pop()
    return AstNode(t.kind, t, parse_precedence(tok, PREC_UNARY))


def parse_binary(tok: Tokenizer) -> Tuple[str, AstNode]:
    t = tok.pop()
    rule = EXPRESSION_RULES[t.kind]
    res = parse_precedence(tok, rule[2] + 1)
    return t.kind, (res,)


EXPRESSION_RULES: Dict[str, Tuple[Callable[[Tokenizer], AstNode], Callable[[Tokenizer], Tuple[str, AstNode]], int]] = {
    'ID': (parse_value, None, PREC_NONE),
    'STRING': (parse_value, None, PREC_NONE),
    '#': (parse_unary, None, PREC_NONE),
    '&': (None, parse_binary, PREC_BITWISE_AND),
    '^': (None, parse_binary, PREC_BITWISE_XOR),
    '|': (None, parse_binary, PREC_BITWISE_OR),
    '+': (parse_unary, parse_binary, PREC_TERM),
    '~': (parse_unary, None, PREC_TERM),
    '!': (parse_unary, None, PREC_TERM),
    '-': (parse_unary, parse_binary, PREC_TERM),
    '/': (None, parse_binary, PREC_FACTOR),
    '*': (None, parse_binary, PREC_FACTOR),
    '%': (None, parse_binary, PREC_FACTOR),
    '>>': (None, parse_binary, PREC_SHIFT),
    '<<': (None, parse_binary, PREC_SHIFT),
    '==': (None, parse_binary, PREC_EQUALITY),
    '!=': (None, parse_binary, PREC_EQUALITY),
    '<': (None, parse_binary, PREC_COMPARISON),
    '>': (None, parse_binary, PREC_COMPARISON),
    '<=': (None, parse_binary, PREC_COMPARISON),
    '>=': (None, parse_binary, PREC_COMPARISON),
    '&&': (None, parse_binary, PREC_LOGIC_AND),
    '||': (None, parse_binary, PREC_LOGIC_OR),
    'NUMBER': (parse_value, None, PREC_NONE),
    '(': (parse_grouping, parse_call, PREC_CALL),
    '[': (parse_ref, None, PREC_CALL),
}


def parse_precedence(tok: Tokenizer, precedence: int) -> AstNode:
    token = tok.peek()
    if token.kind not in EXPRESSION_RULES:
        raise ParseError(token, f"Unexpected: {token.value} ({token.kind})")
    prefix_rule = EXPRESSION_RULES[token.kind][0]
    if prefix_rule is None:
        raise ParseError(token, f"Expect expression, but got: {token.kind}")
    a = prefix_rule(tok)

    while tok.peek().kind in EXPRESSION_RULES and precedence <= EXPRESSION_RULES[tok.peek().kind][2]:
        t = tok.peek()
        infix_rule = EXPRESSION_RULES[t.kind][1]
        assert infix_rule is not None, f"No infix rule for {t.kind}?"
        b, c = infix_rule(tok)
        a = AstNode(b, t, a, *c)
    return a


def parse_expression(tok: Tokenizer) -> AstNode:
    return parse_precedence(tok, PREC_ASSIGNMENT)
