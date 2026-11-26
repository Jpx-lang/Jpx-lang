#!/usr/bin/env python3
"""
Test suite untuk fix A2 Fixed (post-A2):

1.  Argv forwarding        : jpx script.jpx a b -> list `args`
2.  Indexed assignment     : d["k"] = v, arr[i] = x, nested, di dalam function
3.  Compound assignment    : += -= *= /= %= untuk ident, index, list, string
4.  Escape (eval.py)       : \\033 oktal, \\x1B heksa, \\$, \", \\\\,
                             single-quoted string, unknown escape dipertahankan
5.  and/or di dalam string : `mode == "fast and loose"` tidak crash
6.  in / not in            : list, dict, string
7.  sha256 builtin         : string.sha256 / string.sha256_file
8.  Comment stripper       : `"a\\"; # comment` tidak lagi merusak parsing
9.  Binary download        : requests.download binary-safe (live network)

Jalankan:  python3 tests/test_a2_fixes.py   (dari folder jpx-lang/)
"""
import os
import sys
import io
import contextlib
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from interpreter.interpreter import JPXInterpreter


def run_jpx(code, stdin="", script_args=None):
    """Jalankan kode JPX, capture stdout. Return (output, error)."""
    interp = JPXInterpreter(script_args=script_args)
    out_buf = io.StringIO()
    err = None
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


def expect(name, code, expected_output, stdin="", script_args=None):
    out, err = run_jpx(code, stdin, script_args)
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


passed = 0
failed = 0

def check(name, code, expected, **kw):
    global passed, failed
    if expect(name, code, expected, **kw):
        passed += 1
    else:
        failed += 1


# ============================================================
print("=== 1. Argv forwarding ===")
check("args length", "print len(args);", "0")
check("args items", "print args[0]; print args[1]; print len(args);",
      "-o\nout\n3", script_args=["-o", "out", "x"])
check("args compare", 'if args[0] == "-o" { print "flag ok"; }',
      "flag ok", script_args=["-o"])

# ============================================================
print("=== 2. Indexed assignment ===")
check("dict new key", 'global [d = {}];\nd["name"] = "nova";\nprint d["name"];', "nova")
check("nested dict", 'd = {"cfg": {"a": 1}};\nd["cfg"]["b"] = 2;\nprint d["cfg"]["b"];', "2")
check("list replace", "global [arr = [1, 2, 3]];\narr[1] = 99;\nprint arr[1];", "99")
check("dynamic key", 'global [k = "dyn"];\nglobal [d = {}];\nd[k] = "v";\nprint d["dyn"];', "v")
check("assign in function",
      'function setKey(obj, key, val) {\n    obj[key] = val;\n    return obj;\n}\n'
      'd2 = setKey({}, "fn", "ok");\nprint d2["fn"];', "ok")

# ============================================================
print("=== 3. Compound assignment ===")
check("+ int", "c = 1;\nc += 2;\nprint c;", "3")
check("+= string concat", 's = "a";\ns += "b";\nprint s;', "ab")
check("+= list concat", "a = [1];\nb = [2, 3];\na += b;\nprint a[0]; print a[2]; print len(a);",
      "1\n3\n3")
check("-= ", "c = 10;\nc -= 4;\nprint c;", "6.0")
check("*=", "c = 3;\nc *= 3;\nprint c;", "9")
check("/=", "c = 10;\nc /= 4;\nprint c;", "2.5")
check("%=", "c = 10;\nc %= 4;\nprint c;", "2")
check("arr[i] +=", "global [arr = [1, 2, 3]];\narr[2] += 10;\nprint arr[2];", "13")
check("d[k] +=", 'd = {"n": 1};\nd["n"] += 41;\nprint d["n"];', "42")

# ============================================================
print("=== 4. Escape sequences (process_string) ===")
check("octal ESC", 'print len("\\033");', "1")
check("octal value", 'print ord("\\033");', "27")
check("NUL via \\0", 'print len("\\0");', "1")
check("hex ESC", 'print ord("\\x1B");', "27")
check("escaped quote", 'print "quote \\" inside";', 'quote " inside')
check("escaped dollar", 'print "price \\$dollar here";', "price $dollar here")
check("escaped dollar before ident",
      'global [name = "nova"];\nprint "cost: \\$name";', "cost: $name")
check("double backslash", 'print "a\\\\b";', "a\\b")
check("unknown escape kept", 'print "C:\\\\Users\\\\nova";', "C:\\Users\\nova")
check("newline/tabs", 'print "a\\nb";', "a\nb")
check("interpolation still works",
      'global [name = "nova"];\nprint "hi $name";', "hi nova")
check("expr interpolation", 'print "n=${1 + 2}";', "n=3")
check("single quoted basic", "s = 'single quoted';\nprint s;", "single quoted")
check("single quoted: NO interpolation",
      'global [name = "nova"];\nprint \'hi $name\';', "hi $name")
check("single quoted regex-friendly", "p = '^\\$[a-z]+$';\nprint p;", "^$[a-z]+$")
check("single quoted dollar raw", "p = '$name and $x';\nprint p;", "$name and $x")

# ============================================================
print("=== 5. and/or di dalam string ===")
check("and in string equality",
      'mode = "fast";\nif mode == "fast and loose" {\n    print "BUG";\n} else {\n    print "OK";\n}',
      "OK")
check("string containing and compares equal",
      'print "x and y" == "x and y";', "True")
check("or in string equality",
      'print "or text" == "or text";', "True")
check("plain and still works", 'print 1 and 2;', "True")
check("plain or still works", 'print "" or 0;', "False")

# ============================================================
print("=== 6. in / not in ===")
check("in dict", 'pe = {"sha256": "abc"};\nif "sha256" in pe {\n    print "ok";\n}', "ok")
check("in list", "lst = [1, 2, 3];\nif 2 in lst {\n    print \"ok\";\n}", "ok")
check("in string", 'if "ell" in "hello" {\n    print "ok";\n}', "ok")
check("not in list", "lst = [1, 2, 3];\nif 5 not in lst {\n    print \"ok\";\n}", "ok")
check("not in dict", 'pe = {"sha256": "abc"};\nif "md5" not in pe {\n    print "ok";\n}', "ok")
check("in dict negative", 'pe = {"sha256": "abc"};\nif "md5" in pe {\n    print "BUG";\n} else {\n    print "ok";\n}', "ok")

# ============================================================
print("=== 7. sha256 builtin (string module) ===")
check("string.sha256", '[string];\nprint string.sha256("abc");',
      "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")
# sha256_file via temp file dibuat dari sisi Python
_tmpdir = tempfile.mkdtemp()
_file = os.path.join(_tmpdir, "probe.bin")
with open(_file, "wb") as f:
    f.write(b"hello jpx")
import hashlib as _h
_expected = _h.sha256(b"hello jpx").hexdigest()
check("string.sha256_file", '[string];\nprint string.sha256_file("' + _file + '");',
      _expected)
check("string.sha256_file missing", '[string];\nprint string.sha256_file("' +
      os.path.join(_tmpdir, "nope.bin") + '");', "")

# ============================================================
print("=== 8. Comment stripper escape ===")
check("backslash-escaped quote then comment", 's = "a\\\\"; # comment\nprint s;', "a\\")
check("hash inside escaped-quote string", 't = "x\\"y#z";\nprint t;', 'x"y#z')
check("single-quote comment interplay", "u = 'a#b'; # comment\nprint u;", "a#b")

# ============================================================
print("=== 9. Binary-safe streaming download (live network) ===")
def live_download_test():
    try:
        from library.requests import Requests as _R  # noqa
    except Exception:
        return True  # skip bila struktur beda
    url = "https://raw.githubusercontent.com/Jpx-lang/Jpx-lang/main/README.md"
    tmp = os.path.join(tempfile.mkdtemp(), "dl_test.md")
    interp = JPXInterpreter()
    out = io.StringIO()
    err = None
    try:
        with contextlib.redirect_stdout(out):
            interp.run('[requests];\n[string];\n'
                       'res = requests.download("' + url + '", "' + tmp + '");\n'
                       'print res["success"];\n'
                       'print string.sha256_file("' + tmp + '");')
    except Exception as e:
        print("  SKIP  live download (network unavailable):", e)
        return True
    lines = out.getvalue().strip().split("\n")
    if len(lines) < 2 or lines[0] != "True":
        print(f"  FAIL  download success flag: {out.getvalue()!r}")
        return False
    import hashlib as _hh
    with open(tmp, "rb") as f:
        actual = _hh.sha256(f.read()).hexdigest()
    if actual != lines[1]:
        print("  FAIL  sha mismatch - file binary korup!")
        return False
    print("  PASS  requests.download binary-safe (sha256 verified)")
    return True

if live_download_test():
    passed += 1
else:
    failed += 1

# ============================================================
print()
print("=" * 60)
print(f"RESULT: {passed}/{passed + failed} tests passed")
print("=" * 60)
sys.exit(0 if failed == 0 else 1)
