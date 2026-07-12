"""
parser.py - JPX Recursive Descent Parser

Konsumsi list of Token dari lexer.py, hasilkan AST dari ast.py.

Belum di-wire ke interpreter.py — foundation untuk evaluator berbasis AST.
Sudah mendukung seluruh syntax JPX (existing + extension: modulo, bitwise,
string indexing, slice, multiple assignment, default args, lambda).
"""

from typing import List, Optional
from .lexer import tokenize, Token
from . import astnodes as A


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens: List[Token]):
        # Filter NEWLINE tokens — kita pakai ; sebagai separator utuh,
        # newline tidak signifikan (ASI bisa ditambah nanti).
        self.tokens = [t for t in tokens if t.type != 'NEWLINE']
        self.pos = 0

    # ============================================================
    # TOKEN HELPERS
    # ============================================================
    def peek(self, offset=0) -> Token:
        p = self.pos + offset
        return self.tokens[p] if p < len(self.tokens) else self.tokens[-1]

    def advance(self) -> Token:
        t = self.tokens[self.pos]
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return t

    def at_end(self):
        return self.peek().type == 'EOF'

    def check(self, type_, value=None):
        t = self.peek()
        if t.type != type_:
            return False
        if value is not None and t.value != value:
            return False
        return True

    def match(self, type_, value=None):
        if self.check(type_, value):
            return self.advance()
        return None

    def expect(self, type_, value=None):
        if not self.check(type_, value):
            t = self.peek()
            want = f"{type_} {value!r}" if value else type_
            raise ParseError(
                f"Expected {want} at line {t.line}, got {t.type} {t.value!r}"
            )
        return self.advance()

    # ============================================================
    # ENTRY POINT
    # ============================================================
    def parse_program(self) -> A.Program:
        body = []
        while not self.at_end():
            stmt = self.parse_statement()
            if stmt is not None:
                body.append(stmt)
        return A.Program(body=body)

    # ============================================================
    # STATEMENTS
    # ============================================================
    def parse_statement(self):
        t = self.peek()

        if t.type == 'KEYWORD':
            if t.value == 'function':
                return self.parse_function_def()
            if t.value == 'return':
                return self.parse_return()
            if t.value == 'if':
                return self.parse_if()
            if t.value == 'while':
                return self.parse_while()
            if t.value == 'for':
                return self.parse_for()
            if t.value == 'break':
                self.advance(); self.match('PUNCT', ';')
                return A.BreakStatement(line=t.line)
            if t.value == 'continue':
                self.advance(); self.match('PUNCT', ';')
                return A.ContinueStatement(line=t.line)
            if t.value == 'try':
                return self.parse_try_catch()
            if t.value == 'global':
                return self.parse_global()

        # Import statement:  [module]  or  [module.attr]
        # Hanya jika yang mengikuti `[` adalah IDENT (nama modul).
        # Kalau bukan (mis. NUMBER, STRING, `[` nested), itu list literal.
        if self.check('PUNCT', '[') and self.peek(1).type == 'IDENT' \
                and self.peek(2).type in ('PUNCT', 'EOF') \
                and self.peek(2).value in (']', '.', None):
            return self.parse_import()

        # Expression statement
        expr = self.parse_expression()
        self.match('PUNCT', ';')
        return A.ExpressionStatement(expr=expr, line=t.line)

    def parse_block(self) -> List[A.Statement]:
        self.expect('PUNCT', '{')
        body = []
        while not self.check('PUNCT', '}') and not self.at_end():
            stmt = self.parse_statement()
            if stmt is not None:
                body.append(stmt)
        self.expect('PUNCT', '}')
        return body

    def parse_function_def(self):
        kw = self.expect('KEYWORD', 'function')
        name_tok = self.expect('IDENT')
        params, defaults = self.parse_params()
        body = self.parse_block()
        return A.FunctionDef(name=name_tok.value, params=params,
                             defaults=defaults, body=body, line=kw.line)

    def parse_params(self):
        self.expect('PUNCT', '(')
        params = []
        defaults = []
        if not self.check('PUNCT', ')'):
            while True:
                pname = self.expect('IDENT').value
                params.append(pname)
                # Default value
                if self.match('OP', '='):
                    defaults.append(self.parse_expression())
                else:
                    defaults.append(None)
                if not self.match('PUNCT', ','):
                    break
        self.expect('PUNCT', ')')
        return params, defaults

    def parse_return(self):
        kw = self.expect('KEYWORD', 'return')
        if self.check('PUNCT', ';') or self.check('PUNCT', '}'):
            self.match('PUNCT', ';')
            return A.ReturnStatement(line=kw.line)
        value = self.parse_expression()
        self.match('PUNCT', ';')
        return A.ReturnStatement(value=value, line=kw.line)

    def parse_if(self):
        kw = self.expect('KEYWORD', 'if')
        cond = self.parse_expression()
        then_body = self.parse_block()
        else_body = []
        if self.match('KEYWORD', 'else'):
            if self.check('KEYWORD', 'if'):
                # elif: nested IfStatement di else_body
                else_body = [self.parse_if()]
            else:
                else_body = self.parse_block()
        return A.IfStatement(cond=cond, then_body=then_body,
                             else_body=else_body, line=kw.line)

    def parse_while(self):
        kw = self.expect('KEYWORD', 'while')
        cond = self.parse_expression()
        body = self.parse_block()
        return A.WhileStatement(cond=cond, body=body, line=kw.line)

    def parse_for(self):
        kw = self.expect('KEYWORD', 'for')
        var_tok = self.expect('IDENT')
        # for var = start to end { body }
        if self.match('OP', '='):
            start = self.parse_expression()
            self.expect('KEYWORD', 'to')
            end = self.parse_expression()
            body = self.parse_block()
            return A.ForStatement(var=var_tok.value, start=start, end=end,
                                  body=body, line=kw.line)
        # for item in iterable { body }
        if self.match('KEYWORD', 'in'):
            iterable = self.parse_expression()
            body = self.parse_block()
            return A.ForInStatement(var=var_tok.value, iterable=iterable,
                                    body=body, line=kw.line)
        raise ParseError(f"Expected '=' or 'in' after for-var at line {kw.line}")

    def parse_try_catch(self):
        kw = self.expect('KEYWORD', 'try')
        try_body = self.parse_block()
        self.expect('KEYWORD', 'catch')
        param = 'e'
        if self.match('PUNCT', '('):
            param = self.expect('IDENT').value
            self.expect('PUNCT', ')')
        catch_body = self.parse_block()
        return A.TryCatchStatement(try_body=try_body, param=param,
                                   catch_body=catch_body, line=kw.line)

    def parse_global(self):
        kw = self.expect('KEYWORD', 'global')
        self.expect('PUNCT', '[')
        name = self.expect('IDENT').value
        value = None
        if self.match('OP', '='):
            value = self.parse_expression()
        self.expect('PUNCT', ']')
        self.match('PUNCT', ';')
        return A.GlobalStatement(name=name, value=value, line=kw.line)

    def parse_import(self):
        bracket = self.expect('PUNCT', '[')
        module_parts = [self.expect('IDENT').value]
        while self.match('PUNCT', '.'):
            module_parts.append(self.expect('IDENT').value)
        self.expect('PUNCT', ']')
        self.match('PUNCT', ';')
        return A.ImportStatement(module='.'.join(module_parts), line=bracket.line)

    # ============================================================
    # EXPRESSIONS  (Precedence: dari terendah ke tertinggi)
    # ============================================================
    def parse_expression(self):
        return self.parse_ternary()

    def parse_ternary(self):
        cond = self.parse_assignment()
        if self.match('PUNCT', '?'):
            then_expr = self.parse_assignment()
            self.expect('PUNCT', ':')
            else_expr = self.parse_assignment()
            return A.TernaryOp(cond=cond, then_expr=then_expr,
                               else_expr=else_expr, line=cond.line)
        return cond

    def parse_assignment(self):
        left = self.parse_or()
        if self.peek().type == 'OP' and self.peek().value in ('=', '+=', '-=',
                                                               '*=', '/=', '%='):
            op = self.advance().value
            right = self.parse_assignment()
            return A.Assignment(target=left, value=right, op=op, line=left.line)
        return left

    def parse_or(self):
        left = self.parse_and()
        while True:
            if self.check('KEYWORD', 'or'):
                self.advance()
                right = self.parse_and()
                left = A.LogicalOp(op='or', left=left, right=right, line=left.line)
            elif self.match('OP', '||'):
                right = self.parse_and()
                left = A.LogicalOp(op='or', left=left, right=right, line=left.line)
            else:
                break
        return left

    def parse_and(self):
        left = self.parse_equality()
        while True:
            if self.check('KEYWORD', 'and'):
                self.advance()
                right = self.parse_equality()
                left = A.LogicalOp(op='and', left=left, right=right, line=left.line)
            elif self.match('OP', '&&'):
                right = self.parse_equality()
                left = A.LogicalOp(op='and', left=left, right=right, line=left.line)
            else:
                break
        return left

    def parse_equality(self):
        left = self.parse_comparison()
        while self.peek().type == 'OP' and self.peek().value in ('==', '!=', '===', '!=='):
            op = self.advance().value
            right = self.parse_comparison()
            left = A.BinaryOp(op=op, left=left, right=right, line=left.line)
        return left

    def parse_comparison(self):
        left = self.parse_bit_or()
        while self.peek().type == 'OP' and self.peek().value in ('<', '>', '<=', '>='):
            op = self.advance().value
            right = self.parse_bit_or()
            left = A.BinaryOp(op=op, left=left, right=right, line=left.line)
        return left

    def parse_bit_or(self):
        left = self.parse_bit_xor()
        while self.peek().type == 'OP' and self.peek().value in ('|',):
            op = self.advance().value
            right = self.parse_bit_xor()
            left = A.BinaryOp(op=op, left=left, right=right, line=left.line)
        return left

    def parse_bit_xor(self):
        left = self.parse_bit_and()
        while self.peek().type == 'OP' and self.peek().value in ('^',):
            op = self.advance().value
            right = self.parse_bit_and()
            left = A.BinaryOp(op=op, left=left, right=right, line=left.line)
        return left

    def parse_bit_and(self):
        left = self.parse_shift()
        while self.peek().type == 'OP' and self.peek().value in ('&',):
            op = self.advance().value
            right = self.parse_shift()
            left = A.BinaryOp(op=op, left=left, right=right, line=left.line)
        return left

    def parse_shift(self):
        left = self.parse_additive()
        while self.peek().type == 'OP' and self.peek().value in ('<<', '>>'):
            op = self.advance().value
            right = self.parse_additive()
            left = A.BinaryOp(op=op, left=left, right=right, line=left.line)
        return left

    def parse_additive(self):
        left = self.parse_multiplicative()
        while self.peek().type == 'OP' and self.peek().value in ('+', '-'):
            op = self.advance().value
            right = self.parse_multiplicative()
            left = A.BinaryOp(op=op, left=left, right=right, line=left.line)
        return left

    def parse_multiplicative(self):
        left = self.parse_unary()
        while self.peek().type == 'OP' and self.peek().value in ('*', '/', '%', '//'):
            op = self.advance().value
            right = self.parse_unary()
            left = A.BinaryOp(op=op, left=left, right=right, line=left.line)
        return left

    def parse_unary(self):
        if self.peek().type == 'OP' and self.peek().value in ('-', '!', '~'):
            op = self.advance().value
            operand = self.parse_unary()
            return A.UnaryOp(op=op, operand=operand)
        if self.check('KEYWORD', 'not'):
            self.advance()
            operand = self.parse_unary()
            return A.UnaryOp(op='not', operand=operand)
        return self.parse_postfix()

    def parse_postfix(self):
        expr = self.parse_primary()
        while True:
            if self.match('PUNCT', '.'):
                prop = self.expect('IDENT').value
                expr = A.MemberAccess(obj=expr, prop=prop, line=expr.line)
            elif self.match('PUNCT', '('):
                args = self.parse_args()
                self.expect('PUNCT', ')')
                expr = A.Call(callee=expr, args=args, line=expr.line)
            elif self.match('PUNCT', '['):
                # Index or slice
                if self.match('PUNCT', ':'):
                    # [:end]
                    end = None if self.check('PUNCT', ']') else self.parse_expression()
                    self.expect('PUNCT', ']')
                    expr = A.Slice(obj=expr, start=None, end=end, line=expr.line)
                else:
                    idx = self.parse_expression()
                    if self.match('PUNCT', ':'):
                        end = None if self.check('PUNCT', ']') else self.parse_expression()
                        self.expect('PUNCT', ']')
                        expr = A.Slice(obj=expr, start=idx, end=end, line=expr.line)
                    else:
                        self.expect('PUNCT', ']')
                        expr = A.IndexAccess(obj=expr, index=idx, line=expr.line)
            else:
                break
        return expr

    def parse_args(self):
        args = []
        if not self.check('PUNCT', ')'):
            while True:
                args.append(self.parse_expression())
                if not self.match('PUNCT', ','):
                    break
        return args

    def parse_primary(self):
        t = self.peek()

        if t.type == 'NUMBER':
            self.advance()
            if '.' in t.value or 'e' in t.value or 'E' in t.value:
                return A.Literal(value=float(t.value), line=t.line)
            return A.Literal(value=int(t.value), line=t.line)

        if t.type == 'STRING':
            self.advance()
            return A.Literal(value=t.value, line=t.line)

        if t.type == 'KEYWORD':
            if t.value == 'true':
                self.advance(); return A.Literal(value=True, line=t.line)
            if t.value == 'false':
                self.advance(); return A.Literal(value=False, line=t.line)
            if t.value == 'null':
                self.advance(); return A.Literal(value=None, line=t.line)
            # Anonymous function: function(params) { body }
            if t.value == 'function':
                self.advance()
                params, defaults = self.parse_params()
                body = self.parse_block()
                return A.Lambda(params=params, body=body, line=t.line)

        if t.type == 'IDENT':
            self.advance()
            return A.Identifier(name=t.value, line=t.line)

        if self.match('PUNCT', '('):
            expr = self.parse_expression()
            self.expect('PUNCT', ')')
            return expr

        if self.match('PUNCT', '['):
            elements = []
            if not self.check('PUNCT', ']'):
                while True:
                    elements.append(self.parse_expression())
                    if not self.match('PUNCT', ','):
                        break
            self.expect('PUNCT', ']')
            return A.ListLiteral(elements=elements, line=t.line)

        if self.match('PUNCT', '{'):
            pairs = []
            if not self.check('PUNCT', '}'):
                while True:
                    # key: STRING | IDENT
                    if self.check('STRING'):
                        key = self.advance().value
                    elif self.check('IDENT'):
                        key = self.advance().value
                    else:
                        raise ParseError(
                            f"Expected key in object literal at line {t.line}"
                        )
                    self.expect('PUNCT', ':')
                    val = self.parse_expression()
                    pairs.append((key, val))
                    if not self.match('PUNCT', ','):
                        break
            self.expect('PUNCT', '}')
            return A.ObjectLiteral(pairs=pairs, line=t.line)

        raise ParseError(
            f"Unexpected token {t.type} {t.value!r} at line {t.line}"
        )


# ============================================================
# CONVENIENCE
# ============================================================
def parse(source: str) -> A.Program:
    return Parser(tokenize(source)).parse_program()


if __name__ == '__main__':
    import sys
    src = open(sys.argv[1]).read() if len(sys.argv) > 1 else \
        'function f(x, y=10) { return x + y * 2; }\nprint f(3);'
    tree = parse(src)
    print(A.dump(tree))
