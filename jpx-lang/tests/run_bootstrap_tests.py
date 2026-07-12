#!/usr/bin/env python3
"""
Test runner untuk bootstrap self-hosted tests.
Run: python3 tests/run_bootstrap_tests.py
"""
import os, sys, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOTSTRAP = os.path.join(ROOT, 'bootstrap')


def run_jpx_test(path, use_jpx_interp=False):
    """Run a .jpx test file. Return True if pass."""
    name = os.path.basename(path)
    print(f"\n--- {name} ---")

    env = os.environ.copy()
    env['JPX_PATH'] = BOOTSTRAP

    cmd = [sys.executable, os.path.join(ROOT, 'jpx.py')]
    if use_jpx_interp:
        cmd.append('--jpx-interpreter')
    cmd.append(path)

    r = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=300)
    print(r.stdout)
    if r.stderr:
        print(f"STDERR: {r.stderr}")

    if use_jpx_interp:
        return "ALL TESTS PASSED" in r.stdout and r.returncode == 0
    return "ALL TESTS PASSED" in r.stdout


def main():
    passed = 0
    total = 0

    # Bootstrap tests (lexer, ast, parser — pakai main interpreter)
    for name in ['test_lexer.jpx', 'test_ast.jpx', 'test_parser.jpx']:
        total += 1
        if run_jpx_test(os.path.join(BOOTSTRAP, name)):
            passed += 1

    # Evaluator test — pakai --jpx-interpreter flag
    total += 1
    if run_jpx_test(os.path.join(BOOTSTRAP, 'test_evaluator.jpx'),
                    use_jpx_interp=True):
        passed += 1

    print(f"\n{'='*60}")
    print(f"BOOTSTRAP TESTS: {passed}/{total} passed")
    print(f"{'='*60}")
    return 0 if passed == total else 1


if __name__ == '__main__':
    sys.exit(main())
