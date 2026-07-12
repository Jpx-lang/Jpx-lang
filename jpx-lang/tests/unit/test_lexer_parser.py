#!/usr/bin/env python3
"""
Unit test untuk lexer.py dan parser.py.
Memastikan pipeline tokenize -> parse menghasilkan AST yang benar.
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from interpreter.lexer import tokenize, Lexer
from interpreter.parser import parse, Parser, ParseError
from interpreter import astnodes as A


passed = 0
total = 0


def check(name, cond):
    global passed, total
    total += 1
    if cond:
        print(f"  PASS  {name}")
        passed += 1
    else:
        print(f"  FAIL  {name}")


print("=== Lexer ===")

# Tokenize basic
tokens = tokenize('x = 42;')
types = [t.type for t in tokens if t.type != 'NEWLINE']
check("basic tokens", types == ['IDENT', 'OP', 'NUMBER', 'PUNCT', 'EOF'])

tokens = tokenize('"hello world"')
str_tok = [t for t in tokens if t.type == 'STRING']
check("string literal", len(str_tok) == 1 and str_tok[0].value == "hello world")

tokens = tokenize('3.14 42 1e10')
nums = [t for t in tokens if t.type == 'NUMBER']
check("number literals", len(nums) == 3)

tokens = tokenize('function if else while for')
kws = [t for t in tokens if t.type == 'KEYWORD']
check("keywords", len(kws) == 5)

tokens = tokenize('a == b != c <= d >= e')
ops = [t.value for t in tokens if t.type == 'OP']
check("comparison ops", ops == ['==', '!=', '<=', '>='])

tokens = tokenize('# comment\nx = 1;')
idents = [t for t in tokens if t.type == 'IDENT']
check("comment skip", len(idents) == 1 and idents[0].value == 'x')

tokens = tokenize('"line1\\nline2"')
s = [t for t in tokens if t.type == 'STRING'][0]
check("string escape", s.value == "line1\nline2")

print("\n=== Parser: literals ===")
tree = parse('42')
check("int literal",
      isinstance(tree.body[0], A.ExpressionStatement) and
      isinstance(tree.body[0].expr, A.Literal) and
      tree.body[0].expr.value == 42)

tree = parse('"hello"')
check("str literal",
      isinstance(tree.body[0].expr, A.Literal) and
      tree.body[0].expr.value == "hello")

tree = parse('true')
check("bool literal",
      isinstance(tree.body[0].expr, A.Literal) and
      tree.body[0].expr.value is True)

print("\n=== Parser: arithmetic ===")
tree = parse('1 + 2 * 3')
# Should be: BinaryOp(+, 1, BinaryOp(*, 2, 3))
top = tree.body[0].expr
check("precedence: * over +",
      isinstance(top, A.BinaryOp) and top.op == '+' and
      isinstance(top.right, A.BinaryOp) and top.right.op == '*')

tree = parse('(1 + 2) * 3')
top = tree.body[0].expr
check("paren overrides precedence",
      isinstance(top, A.BinaryOp) and top.op == '*' and
      isinstance(top.left, A.BinaryOp) and top.left.op == '+')

print("\n=== Parser: statements ===")
tree = parse('function f(x, y=10) { return x + y; }')
fd = tree.body[0]
check("function def",
      isinstance(fd, A.FunctionDef) and fd.name == 'f' and
      fd.params == ['x', 'y'] and fd.defaults[1] is not None)

tree = parse('if x > 0 { print "pos"; } else { print "neg"; }')
ifs = tree.body[0]
# Each body has 2 statements: `print` (identifier) and `"pos"` (string literal)
# because parser doesn't know `print` is a keyword.
check("if-else",
      isinstance(ifs, A.IfStatement) and
      isinstance(ifs.cond, A.BinaryOp) and
      len(ifs.then_body) == 2 and len(ifs.else_body) == 2)

tree = parse('for i = 0 to 10 { print i; }')
fs = tree.body[0]
check("for-to",
      isinstance(fs, A.ForStatement) and fs.var == 'i')

tree = parse('for item in items { print item; }')
fs = tree.body[0]
check("for-in",
      isinstance(fs, A.ForInStatement) and fs.var == 'item')

tree = parse('try { foo(); } catch (e) { print e; }')
tc = tree.body[0]
check("try-catch",
      isinstance(tc, A.TryCatchStatement) and tc.param == 'e')

tree = parse('[json];')
imp = tree.body[0]
check("import",
      isinstance(imp, A.ImportStatement) and imp.module == 'json')

print("\n=== Parser: expressions ===")
tree = parse('a.b.c')
ma = tree.body[0].expr
check("member access chain",
      isinstance(ma, A.MemberAccess) and ma.prop == 'c' and
      isinstance(ma.obj, A.MemberAccess) and ma.obj.prop == 'b')

tree = parse('a[0]')
ia = tree.body[0].expr
check("index access", isinstance(ia, A.IndexAccess))

tree = parse('a[1:5]')
sl = tree.body[0].expr
check("slice", isinstance(sl, A.Slice))

tree = parse('f(1, 2, 3)')
call = tree.body[0].expr
check("function call",
      isinstance(call, A.Call) and len(call.args) == 3)

tree = parse('[1, 2, 3]')
ll = tree.body[0].expr
check("list literal",
      isinstance(ll, A.ListLiteral) and len(ll.elements) == 3)

tree =parse('{"a": 1, "b": 2}')
ol = tree.body[0].expr
check("object literal",
      isinstance(ol, A.ObjectLiteral) and len(ol.pairs) == 2)

tree = parse('x = 5')
assign = tree.body[0].expr
check("assignment",
      isinstance(assign, A.Assignment) and assign.op == '=')

tree = parse('x ? 1 : 2')
tern = tree.body[0].expr
check("ternary", isinstance(tern, A.TernaryOp))

tree = parse('a and b or c')
or_node = tree.body[0].expr
check("logical: or lowest precedence",
      isinstance(or_node, A.LogicalOp) and or_node.op == 'or' and
      isinstance(or_node.left, A.LogicalOp) and or_node.left.op == 'and')


print(f"\n{'='*50}")
print(f"RESULT: {passed}/{total} passed")
print(f"{'='*50}")
sys.exit(0 if passed == total else 1)
