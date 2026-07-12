"""
ast.py - AST node definitions untuk JPX.

Setiap node adalah dataclass dengan field yang merepresentasikan
struktur sintaks. Parser akan membangun node-node ini dari token,
dan evaluator (masih akan datang) akan mentraverse-nya.
"""

from dataclasses import dataclass, field
from typing import Any, List, Optional


# ============================================================
# EXPRESSIONS
# ============================================================
@dataclass
class Expr:
    """Base class untuk semua expression."""
    line: int = 0


@dataclass
class Literal(Expr):
    value: Any = None
    # value bisa int, float, str, bool, None


@dataclass
class Identifier(Expr):
    name: str = ''


@dataclass
class ListLiteral(Expr):
    elements: List[Expr] = field(default_factory=list)


@dataclass
class ObjectLiteral(Expr):
    pairs: List[tuple] = field(default_factory=list)  # list of (key_str, value_expr)


@dataclass
class BinaryOp(Expr):
    op: str = ''
    left: Optional[Expr] = None
    right: Optional[Expr] = None


@dataclass
class UnaryOp(Expr):
    op: str = ''
    operand: Optional[Expr] = None


@dataclass
class LogicalOp(Expr):
    op: str = ''  # 'and', 'or'
    left: Optional[Expr] = None
    right: Optional[Expr] = None


@dataclass
class TernaryOp(Expr):
    cond: Optional[Expr] = None
    then_expr: Optional[Expr] = None
    else_expr: Optional[Expr] = None


@dataclass
class Assignment(Expr):
    target: Optional[Expr] = None   # Identifier or MemberAccess
    value: Optional[Expr] = None
    op: str = '='  # = += -= *= /= %=


@dataclass
class Call(Expr):
    callee: Optional[Expr] = None
    args: List[Expr] = field(default_factory=list)


@dataclass
class MemberAccess(Expr):
    obj: Optional[Expr] = None
    prop: str = ''  # property name (identifier)


@dataclass
class IndexAccess(Expr):
    obj: Optional[Expr] = None
    index: Optional[Expr] = None  # bisa [start:end] kalau Slice


@dataclass
class Slice(Expr):
    obj: Optional[Expr] = None
    start: Optional[Expr] = None
    end: Optional[Expr] = None


@dataclass
class Lambda(Expr):
    params: List[str] = field(default_factory=list)
    body: List['Statement'] = field(default_factory=list)


# ============================================================
# STATEMENTS
# ============================================================
@dataclass
class Statement:
    """Base class untuk semua statement."""
    line: int = 0


@dataclass
class Program(Statement):
    body: List[Statement] = field(default_factory=list)


@dataclass
class ExpressionStatement(Statement):
    expr: Optional[Expr] = None


@dataclass
class FunctionDef(Statement):
    name: str = ''
    params: List[str] = field(default_factory=list)
    defaults: List[Optional[Expr]] = field(default_factory=list)
    body: List[Statement] = field(default_factory=list)


@dataclass
class ReturnStatement(Statement):
    value: Optional[Expr] = None


@dataclass
class IfStatement(Statement):
    cond: Optional[Expr] = None
    then_body: List[Statement] = field(default_factory=list)
    else_body: List[Statement] = field(default_factory=list)  # bisa IfStatement untuk elif


@dataclass
class WhileStatement(Statement):
    cond: Optional[Expr] = None
    body: List[Statement] = field(default_factory=list)


@dataclass
class ForStatement(Statement):
    """for var = start to end { body }"""
    var: str = ''
    start: Optional[Expr] = None
    end: Optional[Expr] = None
    body: List[Statement] = field(default_factory=list)


@dataclass
class ForInStatement(Statement):
    """for item in iterable { body }"""
    var: str = ''
    iterable: Optional[Expr] = None
    body: List[Statement] = field(default_factory=list)


@dataclass
class BreakStatement(Statement):
    pass


@dataclass
class ContinueStatement(Statement):
    pass


@dataclass
class TryCatchStatement(Statement):
    try_body: List[Statement] = field(default_factory=list)
    param: str = 'e'
    catch_body: List[Statement] = field(default_factory=list)


@dataclass
class GlobalStatement(Statement):
    name: str = ''
    value: Optional[Expr] = None


@dataclass
class ImportStatement(Statement):
    module: str = ''  # bisa "module" atau "module.attr"


# ============================================================
# VISITOR (optional, untuk evaluator nanti)
# ============================================================
class ASTVisitor:
    """Base class untuk visitor pattern. Subclass override visit_*."""
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise NotImplementedError(f"No visitor for {type(node).__name__}")


# ============================================================
# PRETTY PRINTER (debug helper)
# ============================================================
def dump(node, indent=0):
    """Print AST as tree."""
    pad = '  ' * indent
    if node is None:
        return f"{pad}None"
    if not isinstance(node, (Expr, Statement)):
        return f"{pad}{node!r}"
    fields = []
    for f in node.__dataclass_fields__:
        if f == 'line':
            continue
        val = getattr(node, f)
        if isinstance(val, list):
            if not val:
                continue
            fields.append(f"{pad}  {f}:")
            for item in val:
                fields.append(dump(item, indent + 2))
        elif isinstance(val, (Expr, Statement)):
            fields.append(f"{pad}  {f}:")
            fields.append(dump(val, indent + 2))
        else:
            fields.append(f"{pad}  {f}: {val!r}")
    return f"{pad}{type(node).__name__}\n" + '\n'.join(fields)


if __name__ == '__main__':
    # Smoke test: build a small AST manually
    prog = Program(body=[
        FunctionDef(
            name='add',
            params=['a', 'b'],
            body=[
                ReturnStatement(value=BinaryOp(
                    op='+', left=Identifier(name='a'), right=Identifier(name='b')
                ))
            ]
        ),
        ExpressionStatement(expr=Call(
            callee=Identifier(name='print'),
            args=[Call(
                callee=Identifier(name='add'),
                args=[Literal(value=3), Literal(value=4)]
            )]
        ))
    ])
    print(dump(prog))
