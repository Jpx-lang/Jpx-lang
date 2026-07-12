#!/usr/bin/env python3
"""
Test runner untuk JPX.
Menjalankan:
  - tests/unit/*.py        unit test untuk interpreter (Python)
  - tests/unit/*.jpx       JPX self-test (assertion via output)
  - tests/e2e/*.jpx        end-to-end programs
"""
import os, sys, subprocess, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

def run_py_test(path):
    """Run a Python unit test file."""
    print(f"\n--- Python unit: {os.path.basename(path)} ---")
    r = subprocess.run([sys.executable, path], capture_output=True, text=True, cwd=ROOT)
    print(r.stdout)
    if r.returncode != 0:
        print(f"STDERR: {r.stderr}")
        return False
    return True


def run_jpx_test(path):
    """Run a .jpx test file.
    - Untuk file di tests/unit/: lulus jika stdout mengandung 'ALL TESTS PASSED'
      dan tidak ada line yang dimulai dengan '  FAIL  '.
    - Untuk file di tests/e2e/: lulus jika exit code 0 (showcase programs).
    """
    print(f"\n--- JPX test: {os.path.basename(path)} ---")
    r = subprocess.run(
        [sys.executable, os.path.join(ROOT, "jpx.py"), path],
        capture_output=True, text=True, cwd=ROOT, timeout=30,
    )
    # Print stdout (truncated if very long)
    out = r.stdout
    if len(out) > 5000:
        print(out[:5000])
        print(f"... [truncated, total {len(out)} chars]")
    else:
        print(out)
    if r.stderr:
        print(f"STDERR: {r.stderr}")
    if r.returncode != 0:
        return False
    # e2e tests: just check exit code
    if "e2e" in path:
        return True
    # unit tests: check for PASS marker and no FAIL lines
    if "ALL TESTS PASSED" not in r.stdout:
        return False
    for line in r.stdout.split("\n"):
        if line.startswith("  FAIL  "):
            return False
    return True


def main():
    total = 0
    passed = 0
    test_dir = os.path.join(ROOT, "tests")

    # Python unit tests
    for path in sorted(glob.glob(os.path.join(test_dir, "unit", "*.py"))):
        total += 1
        if run_py_test(path):
            passed += 1

    # JPX tests
    for path in sorted(glob.glob(os.path.join(test_dir, "**", "*.jpx"), recursive=True)):
        total += 1
        if run_jpx_test(path):
            passed += 1

    print(f"\n{'='*60}")
    print(f"TOTAL: {passed}/{total} test files passed")
    print(f"{'='*60}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
