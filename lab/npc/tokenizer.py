from dataclasses import dataclass
from typing import Optional
import os
import re
import ast


class ParseError(Exception):
    def __init__(self, token, message):
        self.token = token
        self.message = message


@dataclass
class Token:
    kind: str
    value: float
    line: int
    column: int


class Tokenizer:
    TOKEN_REGEX = re.compile('|'.join('(?P<%s>%s)' % pair for pair in [
        ('OHEX', r'0x[0-9A-Fa-f][0-9A-Fa-f_]*'),
        ('NUMBER', r'\d+(\.\d*)?'),
        ('HEX', r'\$[0-9A-Fa-f][0-9A-Fa-f_]*'),
        ('BIN', r'%[0-1][0-1_]*'),
        ('GFX', r'`[0-3]+'),
        ('COMMENT', r'#[^\n]*'),
        ('STRING', r'"(\\.|[^"\\])*"'),
        ('ID', r'\.?[A-Za-z_][A-Za-z0-9_\.]*'),
        ('CURADDR', r'@'),
        ('OP', r'(?:<=)|(?:>=)|(?:==)|(?:!=)|(?:<<)|(?:>>)|(?:&&)|(?:\|\|)|[+\-*/,\(\)<>&|\[\]{}=!~\^\%:;]'),
        ('SKIPNEWLINE', r'\\\n'),
        ('NEWLINE', r'\n[ \t]*'),
        ('SKIP', r'[ \t]+'),
        ('MISMATCH', r'.'),
    ]))

    def __init__(self, filename: str):
        self.__tokens = []
        self.__eof = Token("EOF", "", 1, 1)
        self._read_file(filename)
    
    def _read_file(self, filename):
        file_data = open(filename, "rt").read()
        line = 1
        column = 1
        for m in self.TOKEN_REGEX.finditer(file_data):
            kind = m.lastgroup
            value = m.group()
            match kind:
                case "NEWLINE":
                    self.__tokens.append(Token("NEWLINE", len(value) - 1, line, column))
                    line += 1
                    column = 0
                case "OP":
                    self.__tokens.append(Token(value, value, line, column))
                case "ID":
                    self.__tokens.append(Token(kind, value, line, column))
                case "HEX":
                    self.__tokens.append(Token("NUMBER", int(value[1:], 16), line, column))
                case "OHEX":
                    self.__tokens.append(Token("NUMBER", int(value, 16), line, column))
                case "NUMBER":
                    self.__tokens.append(Token(kind, int(value), line, column))
                case "STRING":
                    self.__tokens.append(Token(kind, ast.literal_eval(value), line, column))
                case "SKIP":
                    pass
                case _:
                    raise RuntimeError(f"Unknown tokenizer kind: {kind}: {value}")
            column += len(value)
    
    def pop(self) -> Token:
        if not self.__tokens:
            return self.__eof
        return self.__tokens.pop(0)
        
    def peek(self) -> Token:
        if not self.__tokens:
            return self.__eof
        return self.__tokens[0]

    def expect(self, kind: str, value: Optional[str] = None) -> Token:
        token = self.pop()
        if token.kind != kind:
            raise ParseError(token, f"Unexpected {token.value} ({token.kind}), expected a {kind}")
        if value is not None and token.value != value:
            raise ParseError(token, f"Unexpected {token.value}, expected {value}")
        return token

    def match(self, kind: str, value: Optional[str] = None) -> Token:
        token = self.peek()
        if token.kind != kind:
            return None
        if value is not None and token.value != value:
            return None
        return self.pop()


if __name__ == "__main__":
    import sys
    for arg in sys.argv[1:]:
        tok = Tokenizer(arg)
        while tok.peek().kind != "EOF":
            print(tok.pop())
