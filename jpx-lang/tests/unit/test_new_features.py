#!/usr/bin/env python3
"""
Unit test untuk fitur-fitur baru yang ditambahkan pasca-fix.
Run: python3 tests/unit/test_new_features.py
"""
import os, sys, io, contextlib

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from interpreter.interpreter import JPXInterpreter


def run(code):
    interp = JPXInterpreter()
    out = io.StringIO()
    err = None
    with contextlib.redirect_stdout(out):
        try:
            interp.run(code)
        except Exception as e:
            err = f"{type(e).__name__}: {e}"
    return out.getvalue().rstrip(), err


def expect(name, code, expected):
    out, err = run(code)
    if err:
        print(f"  FAIL  {name}: {err}")
        return False
    if out != expected:
        print(f"  FAIL  {name}\n        expect: {expected!r}\n        got:    {out!r}")
        return False
    print(f"  PASS  {name}")
    return True


passed = 0
total = 0

print("=== String indexing ===")
total += 1; passed += expect("s[0]", 'global [s="hello"]; print s[0];', "h")
total += 1; passed += expect("s[1]", 'global [s="hello"]; print s[1];', "e")
total += 1; passed += expect("s[-1]", 'global [s="hello"]; print s[-1];', "o")

print("\n=== String slicing ===")
total += 1; passed += expect("s[0:3]", 'global [s="hello"]; print s[0:3];', "hel")
total += 1; passed += expect("s[2:]", 'global [s="hello"]; print s[2:];', "llo")
total += 1; passed += expect("s[:3]", 'global [s="hello"]; print s[:3];', "hel")
total += 1; passed += expect("s[:]", 'global [s="hello"]; print s[:];', "hello")

print("\n=== Modulo ===")
total += 1; passed += expect("17 % 5", 'print 17 % 5;', "2")
total += 1; passed += expect("10 % 3", 'print 10 % 3;', "1")
total += 1; passed += expect("100 % 7", 'print 100 % 7;', "2")

print("\n=== ord/chr ===")
total += 1; passed += expect("ord(A)", 'print ord("A");', "65")
total += 1; passed += expect("ord(a)", 'print ord("a");', "97")
total += 1; passed += expect("chr(66)", 'print chr(66);', "B")
total += 1; passed += expect("chr(97)", 'print chr(97);', "a")

print("\n=== Type conversion ===")
total += 1; passed += expect("int(42)", 'print int("42");', "42")
total += 1; passed += expect("str(123)", 'print str(123);', "123")
total += 1; passed += expect("float(3.5)", 'print float("3.5");', "3.5")
total += 1; passed += expect("type(s)", 'global [s="x"]; print type(s);', "str")
total += 1; passed += expect("type(1)", 'print type(1);', "int")
total += 1; passed += expect("len(s)", 'global [s="hello"]; print len(s);', "5")
total += 1; passed += expect("len([1,2,3])", 'global [a=[1,2,3]]; print len(a);', "3")

print("\n=== Closures ===")
total += 1; passed += expect(
    "closure captures parent var",
    'global [PI=3.14]; function area(r) { return PI * r * r; } print area(2);',
    "12.56",
)

total += 1; passed += expect(
    "function defined inside function",
    'function outer() { global [x=10]; function inner() { return x + 5; } return inner(); } print outer();',
    "15",
)

print(f"\n{'='*50}")
print(f"RESULT: {passed}/{total} passed")
print(f"{'='*50}")
sys.exit(0 if passed == total else 1)
