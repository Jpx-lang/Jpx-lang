"""
lexer.py - JPX Lexer / Tokenizer
Mengubah source code string menjadi list of Token.

Belum di-wire ke interpreter utama (interpreter.py masih regex-based).
Ini foundation untuk parser.py dan AST-based evaluation yang akan datang.
"""

from dataclasses import dataclass, field
from typing import List, Optional
import re


# ============================================================
# TOKEN TYPES
# ============================================================
KEYWORDS = {
    'function', 'return', 'if', 'else', 'while', 'for', 'in', 'to',
    'break', 'continue', 'try', 'catch', 'global', 'import',
    'true', 'false', 'null', 'and', 'or', 'not',
}

# 3-char ops first, then 2-char, then 1-char (greedy match)
OPERATORS_3 = ['===', '!==', '...', '<<=', '>>=']
OPERATORS_2 = ['==', '!=', '<=', '>=', '&&', '||', '+=', '-=', '*=', '/=',
               '%=', '<<', '>>', '**', '//', '=>']
OPERATORS_1 = ['+', '-', '*', '/', '%', '=', '<', '>', '!', '&', '|', '^', '~']

PUNCTUATION = set('(){}[];,.:?')


@dataclass
class Token:
    type: str            # NUMBER, STRING, IDENT, KEYWORD, OP, PUNCT, EOF, NEWLINE
    value: str
    line: int = 0
    col: int = 0

    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, line={self.line})"


class LexError(Exception):
    pass


# ============================================================
# LEXER
# ============================================================
class Lexer:
    def __init__(self, source: str):
        # Strip BOM
        if source.startswith('\ufeff'):
            source = source[1:]
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens: List[Token] = []

    def error(self, msg):
        raise LexError(f"Lex error at line {self.line}, col {self.col}: {msg}")

    def peek(self, offset=0):
        p = self.pos + offset
        return self.source[p] if p < len(self.source) else '\0'

    def advance(self):
        ch = self.source[self.pos]
        self.pos += 1
        if ch == '\n':
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def at_end(self):
        return self.pos >= len(self.source)

    # ============================================================
    # MAIN
    # ============================================================
    def tokenize(self) -> List[Token]:
        while not self.at_end():
            ch = self.peek()

            # Whitespace (skip, but track newlines for potential ASI)
            if ch in ' \t\r':
                self.advance()
                continue
            if ch == '\n':
                self.tokens.append(Token('NEWLINE', '\\n', self.line, self.col))
                self.advance()
                continue

            # Comments
            if ch == '#':
                self._skip_line_comment()
                continue
            if ch == '/' and self.peek(1) == '/':
                self._skip_line_comment()
                continue
            if ch == '/' and self.peek(1) == '*':
                self._skip_block_comment()
                continue

            # String literals
            if ch == '"':
                self._read_string('"')
                continue
            if ch == "'":
                self._read_string("'")
                continue

            # Numbers
            if ch.isdigit() or (ch == '.' and self.peek(1).isdigit()):
                self._read_number()
                continue

            # Identifiers / keywords
            if ch.isalpha() or ch == '_':
                self._read_identifier()
                continue

            # Operators (greedy)
            if self._try_operator():
                continue

            # Punctuation
            if ch in PUNCTUATION:
                self.tokens.append(Token('PUNCT', ch, self.line, self.col))
                self.advance()
                continue

            self.error(f"Unexpected character: {ch!r}")

        self.tokens.append(Token('EOF', '', self.line, self.col))
        return self.tokens

    # ============================================================
    # HELPERS
    # ============================================================
    def _skip_line_comment(self):
        while not self.at_end() and self.peek() != '\n':
            self.advance()

    def _skip_block_comment(self):
        self.advance()  # /
        self.advance()  # *
        while not self.at_end():
            if self.peek() == '*' and self.peek(1) == '/':
                self.advance()
                self.advance()
                return
            self.advance()
        self.error("Unterminated block comment")

    def _read_string(self, quote):
        start_line, start_col = self.line, self.col
        self.advance()  # opening quote
        chars = []
        while not self.at_end():
            ch = self.peek()
            if ch == quote:
                self.advance()
                self.tokens.append(Token('STRING', ''.join(chars), start_line, start_col))
                return
            if ch == '\\':
                self.advance()
                esc = self.peek()
                mapping = {
                    'n': '\n', 't': '\t', 'r': '\r', '\\': '\\',
                    '"': '"', "'": "'", '0': '\0', 'b': '\b', 'f': '\f',
                }
                if esc in mapping:
                    chars.append(mapping[esc])
                else:
                    chars.append(esc)
                self.advance()
                continue
            if ch == '\n':
                self.error("Unterminated string literal")
            chars.append(ch)
            self.advance()
        self.error("Unterminated string literal")

    def _read_number(self):
        start_line, start_col = self.line, self.col
        chars = []
        is_float = False
        while not self.at_end() and (self.peek().isdigit() or self.peek() == '.'):
            if self.peek() == '.':
                if is_float:
                    break  # second dot — stop here
                is_float = True
            chars.append(self.advance())
        # Exponent
        if self.peek() in ('e', 'E'):
            chars.append(self.advance())
            if self.peek() in ('+', '-'):
                chars.append(self.advance())
            while not self.at_end() and self.peek().isdigit():
                chars.append(self.advance())
            is_float = True
        self.tokens.append(Token('NUMBER', ''.join(chars), start_line, start_col))

    def _read_identifier(self):
        start_line, start_col = self.line, self.col
        chars = []
        while not self.at_end() and (self.peek().isalnum() or self.peek() == '_'):
            chars.append(self.advance())
        word = ''.join(chars)
        if word in KEYWORDS:
            self.tokens.append(Token('KEYWORD', word, start_line, start_col))
        else:
            self.tokens.append(Token('IDENT', word, start_line, start_col))

    def _try_operator(self):
        # Try 3-char, then 2-char, then 1-char
        for ops in (OPERATORS_3, OPERATORS_2, OPERATORS_1):
            for op in ops:
                if self.source[self.pos:self.pos + len(op)] == op:
                    self.tokens.append(Token('OP', op, self.line, self.col))
                    for _ in range(len(op)):
                        self.advance()
                    return True
        return False


# ============================================================
# CONVENIENCE
# ============================================================
def tokenize(source: str) -> List[Token]:
    return Lexer(source).tokenize()


if __name__ == '__main__':
    import sys
    src = open(sys.argv[1]).read() if len(sys.argv) > 1 else 'function f(x) { return x + 1; }'
    for t in tokenize(src):
        if t.type != 'NEWLINE':
            print(t)
