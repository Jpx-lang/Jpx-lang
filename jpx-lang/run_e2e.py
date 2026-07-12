#!/usr/bin/env python3
"""
End-to-end smoke test: jalankan file .jpx lewat jpx.py runner yang sebenarnya.
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))


def run_jpx_file(filename, stdin=""):
    """Run a .jpx file via jpx.py runner. Return (stdout, returncode)."""
    proc = subprocess.run(
        [sys.executable, os.path.join(ROOT, "jpx.py"), filename],
        capture_output=True, text=True, input=stdin, timeout=10,
        cwd=ROOT,
    )
    return proc.stdout.rstrip(), proc.stderr.rstrip(), proc.returncode


# Test 1: program dengan function + comparison + arithmetic + if-else
print("=== Test 1: comprehensive .jpx program ===")
with open(os.path.join(ROOT, "test_comprehensive.jpx"), "w") as f:
    f.write("""# Comprehensive test untuk JPX setelah perbaikan
[print];
[time];

# Function dengan return
function isPositive(n) {
    if n > 0 {
        return true;
    } else {
        return false;
    }
}

function double(n) {
    return n + n;
}

# Arithmetic
global [sum = 0];
for i = 1 to 10 {
    global [sum = sum + i];
}
print "Sum 1..10 = " + sum;

# Function call + comparison
print "isPositive(4) = " + isPositive(4);
print "isPositive(-3) = " + isPositive(-3);
print "double(21) = " + double(21);

# String concat + variable interpolation
global [name = "JPX"];
global [version = "1.0"];
print "Hello from $name v$version";

# if-else-if
global [score = 85];
if score >= 90 {
    print "Grade: A";
} else {
    if score >= 80 {
        print "Grade: B";
    } else {
        print "Grade: C";
    }
}

# While loop with break
global [count = 0];
while true {
    global [count = count + 1];
    if count == 5 {
        break;
    }
}
print "Counted to: " + count;

print "Done!";
""")

out, err, rc = run_jpx_file(os.path.join(ROOT, "test_comprehensive.jpx"))
expected_lines = [
    "Sum 1..10 = 55",
    "isPositive(4) = True",
    "isPositive(-3) = False",
    "double(21) = 42",
    "Hello from JPX v1.0",
    "Grade: B",
    "Counted to: 5",
    "Done!",
]
actual_lines = out.split("\n")

all_ok = True
for i, expected in enumerate(expected_lines):
    if i >= len(actual_lines):
        print(f"  FAIL  expected line {i}: {expected!r}, but no output line")
        all_ok = False
    elif actual_lines[i] != expected:
        print(f"  FAIL  line {i}: expected {expected!r}, got {actual_lines[i]!r}")
        all_ok = False
    else:
        print(f"  PASS  {actual_lines[i]}")

if err:
    print(f"  STDERR: {err}")
    all_ok = False

print()
print(f"Test 1 result: {'PASS' if all_ok else 'FAIL'}")
print()

# Test 2: try-catch + library usage
print("=== Test 2: try-catch + libraries ===")
with open(os.path.join(ROOT, "test_trycatch.jpx"), "w") as f:
    f.write("""# Try-catch test
[json];
[string];

# json encode/decode roundtrip
global [data = {"name": "Alice", "age": 30}];
global [encoded = json.encode(data)];
print "Encoded: " + encoded;

global [decoded = json.decode(encoded)];
print "Decoded name: " + decoded.name;

# String library
global [upper = string.upper("hello world")];
print "Upper: " + upper;

global [md5 = string.md5("test")];
print "MD5: " + md5;

# Try-catch
try {
    global [bad = undefined_var + 1];
} catch (e) {
    print "Caught error: " + e;
}

print "Done!";
""")

out, err, rc = run_jpx_file(os.path.join(ROOT, "test_trycatch.jpx"))
print(f"  Output:\n    {out.replace(chr(10), chr(10) + '    ')}")
if err:
    print(f"  STDERR: {err}")
print(f"  Return code: {rc}")

sys.exit(0 if all_ok else 1)
