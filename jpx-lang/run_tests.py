#!/usr/bin/env python3
"""
Test suite untuk verifikasi perbaikan bug di JPX interpreter.
Setiap test mereproduksi salah satu bug yang sebelumnya rusak.
"""
import os
import sys
import io
import contextlib

# Pastikan pakai source yang diperbaiki
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from interpreter.interpreter import JPXInterpreter


def run_jpx(code, stdin=""):
    """Jalankan kode JPX, capture stdout. Return (output, error)."""
    interp = JPXInterpreter()
    out_buf = io.StringIO()
    err = None
    # Mock stdin agar scanner tidak hang
    orig_stdin = sys.stdin
    sys.stdin = io.StringIO(stdin)
    try:
        with contextlib.redirect_stdout(out_buf):
            interp.run(code)
    except Exception as e:
        err = f"{type(e).__name__}: {e}"
    finally:
        sys.stdin = orig_stdin
    return out_buf.getvalue().rstrip(), err


def expect(name, code, expected_output, stdin=""):
    """Jalankan test, return True jika output sesuai."""
    out, err = run_jpx(code, stdin)
    if err:
        print(f"  FAIL  {name}")
        print(f"        code:    {code!r}")
        print(f"        error:   {err}")
        return False
    if out != expected_output:
        print(f"  FAIL  {name}")
        print(f"        code:    {code!r}")
        print(f"        expect:  {expected_output!r}")
        print(f"        got:     {out!r}")
        return False
    print(f"  PASS  {name}")
    return True


def expect_error(name, code, error_fragment):
    """Jalankan test, return True jika error mengandung fragment."""
    out, err = run_jpx(code)
    if err is None:
        print(f"  FAIL  {name}")
        print(f"        code:    {code!r}")
        print(f"        expect error containing: {error_fragment!r}")
        print(f"        but no error raised. stdout: {out!r}")
        return False
    if error_fragment.lower() not in err.lower():
        print(f"  FAIL  {name}")
        print(f"        code:    {code!r}")
        print(f"        expect error containing: {error_fragment!r}")
        print(f"        got:     {err!r}")
        return False
    print(f"  PASS  {name}")
    return True


passed = 0
total = 0

# ============================================================
# Bug 1: return dari function
# ============================================================
print("\n=== Bug 1: Function return value ===")
total += 1
passed += expect(
    "function add(a,b) returns 7",
    'function add(a, b) { return a + b; }\nresult = add(3, 4);\nprint result;',
    "7",
)

total += 1
passed += expect(
    "function with string return",
    'function greet(name) { return "Hello, " + name; }\nprint greet("JPX");',
    "Hello, JPX",
)

total += 1
passed += expect(
    "function no return -> null",
    'function noop() { print "inside noop"; }\nr = noop();\nprint r == null;',
    "inside noop\nTrue",
)

# ============================================================
# Bug 2: Comparison operators
# ============================================================
print("\n=== Bug 2: Comparison operators ===")
total += 1
passed += expect(
    "if x == y",
    'global [x = 5];\nglobal [y = 5];\nif x == y {\n  print "equal";\n}',
    "equal",
)

total += 1
passed += expect(
    "if x != y",
    'global [x = 5];\nglobal [y = 6];\nif x != y {\n  print "different";\n}',
    "different",
)

total += 1
passed += expect(
    "if x <= y",
    'global [x = 5];\nglobal [y = 5];\nif x <= y {\n  print "le";\n}',
    "le",
)

total += 1
passed += expect(
    "if x >= y",
    'global [x = 10];\nglobal [y = 5];\nif x >= y {\n  print "ge";\n}',
    "ge",
)

total += 1
passed += expect(
    "comparison in expression",
    'global [x = 5];\nprint x == 5;',
    "True",
)

# ============================================================
# Bug 3: Arithmetic addition
# ============================================================
print("\n=== Bug 3: Arithmetic addition ===")
total += 1
passed += expect(
    "3 + 4 == 7",
    'print 3 + 4;',
    "7",
)

total += 1
passed += expect(
    "10 + 20 + 30 == 60",
    'print 10 + 20 + 30;',
    "60",
)

total += 1
passed += expect(
    "string concat still works",
    'print "Hello" + " " + "World";',
    "Hello World",
)

total += 1
passed += expect(
    "mixed: number + number in var",
    'global [a = 10];\nglobal [b = 20];\nprint a + b;',
    "30",
)

total += 1
passed += expect(
    "subtraction",
    'print 10 - 3;',
    "7.0",
)

total += 1
passed += expect(
    "multiplication",
    'print 6 * 7;',
    "42.0",
)

# ============================================================
# Bug 4: string.random()
# ============================================================
print("\n=== Bug 4: string.random() ===")
total += 1
# random returns string of length N. We can't predict content, but check length.
out, err = run_jpx('[string];\nglobal [s = string.random(15)];\nprint s length;')
if err:
    print(f"  FAIL  string.random(15) length -> {err}")
else:
    if out == "15":
        print(f"  PASS  string.random(15) returns 15-char string")
        passed += 1
    else:
        print(f"  FAIL  string.random(15) length expected 15, got {out!r}")

# ============================================================
# Bug 5: __name__ guard
# ============================================================
print("\n=== Bug 5: __name__ guard (no spurious output on import) ===")
total += 1
out, err = run_jpx('[string];\nprint "done";')
# Sebelum perbaikan, ada pesan "[string.py] Library string siap digunakan!"
# yang muncul saat import. Setelah perbaikan tidak boleh ada.
if err:
    print(f"  FAIL  import string -> {err}")
elif "Library string siap" in out:
    print(f"  FAIL  spurious import message still present: {out!r}")
else:
    print(f"  PASS  no spurious import message")
    passed += 1

total += 1
out, err = run_jpx('[json];\nprint "done";')
if err:
    print(f"  FAIL  import json -> {err}")
elif "Library JSON siap" in out:
    print(f"  FAIL  spurious import message still present: {out!r}")
else:
    print(f"  PASS  no spurious import message (json)")
    passed += 1

# ============================================================
# Bug 8: null variable treated as undefined
# ============================================================
print("\n=== Bug 8: null variable ===")
total += 1
passed += expect(
    "null variable is accessible",
    'global [x = null];\nprint x == null;',
    "True",
)

total += 1
passed += expect_error(
    "truly undefined variable still raises NameError",
    'print undefined_var;',
    "not defined",
)

# ============================================================
# Bug 9: if-else multiline
# ============================================================
print("\n=== Bug 9: if-else multiline ===")
total += 1
passed += expect(
    "if-else true branch",
    'global [x = 10];\nif x > 5 {\n  print "big";\n} else {\n  print "small";\n}',
    "big",
)

total += 1
passed += expect(
    "if-else false branch",
    'global [x = 3];\nif x > 5 {\n  print "big";\n} else {\n  print "small";\n}',
    "small",
)

total += 1
passed += expect(
    "if-else-if chain",
    'global [x = 5];\nif x == 1 {\n  print "one";\n} else {\n  if x == 5 {\n    print "five";\n  } else {\n    print "other";\n  }\n}',
    "five",
)

# ============================================================
# Bug 11: Print.string()
# ============================================================
print("\n=== Bug 11: Print.string() ===")
total += 1
passed += expect(
    "print.string() outputs text",
    '[print];\nprint.string("hello from print.string");',
    "hello from print.string",
)

# ============================================================
# Sanity: libraries still work
# ============================================================
print("\n=== Sanity: library imports ===")
total += 1
passed += expect(
    "time.timestamp() returns number",
    '[time];\nglobal [t = time.timestamp];\nprint t > 0;',
    "True",
)

total += 1
passed += expect(
    "json.encode",
    '[json];\nprint json.encode({"name": "jpx"});',
    '{"name": "jpx"}',
)

total += 1
passed += expect(
    "math.floor",
    '[math];\nprint math.floor(3.7);',
    "3",
)

# ============================================================
# Summary
# ============================================================
print(f"\n{'='*60}")
print(f"RESULT: {passed}/{total} tests passed")
print(f"{'='*60}")
sys.exit(0 if passed == total else 1)
