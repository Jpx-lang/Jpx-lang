#!/usr/bin/env python3
# jpx.py - JPX Interpreter Runner
# Usage: jpx <file.jpx> or jpx --version

import sys
import os
import argparse

# Constants
VERSION = "1.0.0"
VERSION_NAME = "JPX v1.0. A exclusive version version"

def get_jpx_paths():
    """Dapatkan path penting JPX"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    paths = {
        'root': base_dir,
        'library': os.path.join(base_dir, 'library'),
        'lib': os.path.join(base_dir, 'lib'),
        'interpreter': os.path.join(base_dir, 'interpreter')
    }
    
    return paths

def show_version():
    """Tampilkan versi JPX"""
    paths = get_jpx_paths()
    
    print(f"{VERSION_NAME}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Root: {paths['root']}")
    print(f"Library: {paths['library']}")
    print(f"User lib: {paths['lib']}")

def show_help():
    """Tampilkan help"""
    print("JPX Programming Language")
    print(f"Version: {VERSION_NAME}")
    print("\nUsage:")
    print("  jpx <file.jpx>              Run a JPX script")
    print("  jpx --version, -v            Show version information")
    print("  jpx --help, -h               Show this help message")
    print("  jpx --info                    Show system information")
    print("\nExamples:")
    print("  jpx script.jpx")
    print("  jpx examples/hello.jpx")
    print("\nEnvironment:")
    print("  JPX_PATH                      Additional library paths")
    print("\nMore info: https://github.com/alzzmetth/Jpx-lang")

def show_info():
    """Tampilkan informasi detail"""
    paths = get_jpx_paths()
    
    print("JPX System Information")
    print("=" * 50)
    print(f"Version: {VERSION_NAME}")
    print(f"Interpreter: {sys.executable}")
    print(f"Platform: {sys.platform}")
    print(f"Python: {sys.version}")
    print("\nPaths:")
    print(f"  Root: {paths['root']}")
    print(f"  Library (built-in): {paths['library']}")
    print(f"  User lib (packages): {paths['lib']}")
    print(f"  Interpreter: {paths['interpreter']}")
    
    # Cek keberadaan folder
    print("\nDirectory status:")
    for name, path in paths.items():
        status = "✓" if os.path.exists(path) else "✗"
        print(f"  {status} {name}: {path}")
    
    # Cek environment variable
    jpx_path = os.environ.get('JPX_PATH')
    if jpx_path:
        print(f"\nJPX_PATH: {jpx_path}")
        for p in jpx_path.split(os.pathsep):
            status = "✓" if os.path.exists(p) else "✗"
            print(f"  {status} {p}")

def run_file(filename):
    """Jalankan file JPX"""
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found")
        sys.exit(1)

    # Tambahkan root directory ke path (agar `from interpreter.x import y` jalan)
    paths = get_jpx_paths()
    sys.path.insert(0, paths['root'])

    # Tambahkan JPX_PATH jika ada (Python sys.path untuk native module)
    jpx_path = os.environ.get('JPX_PATH')
    if jpx_path:
        for p in jpx_path.split(os.pathsep):
            if p and os.path.exists(p):
                sys.path.insert(0, p)

    try:
        # Import interpreter
        from interpreter.interpreter import JPXInterpreter

        # Baca file
        with open(filename, 'r', encoding='utf-8-sig') as f:
            code = f.read()

        # Buat interpreter dan jalankan
        interpreter = JPXInterpreter()

        # Set script_dir agar import bisa cari file .jpx/.py di direktori
        # yang sama dengan script utama (relative import).
        script_dir = os.path.dirname(os.path.abspath(filename))
        interpreter.import_handler.set_script_dir(script_dir)

        # Optional: tampilkan info file
        # print(f"Running: {filename}")
        
        try:
            interpreter.run(code)
        except KeyboardInterrupt:
            print("\nExecution interrupted by user")
            sys.exit(130)
        except Exception as e:
            print(f"Runtime Error: {e}")
            sys.exit(1)
            
    except ImportError as e:
        print(f"Error: Cannot load JPX interpreter: {e}")
        print("Make sure you're running from the correct directory")
        sys.exit(1)

def list_modules():
    """List semua module yang tersedia di search paths."""
    paths = get_jpx_paths()
    sys.path.insert(0, paths['root'])
    from interpreter.importer import ImportHandler
    from interpreter.interpreter import JPXInterpreter

    interp = JPXInterpreter()
    modules = interp.import_handler.list_available_modules()

    print("Available JPX modules:")
    print("=" * 50)
    for name in sorted(modules.keys()):
        ext, path = modules[name]
        rel_path = os.path.relpath(path)
        lang = "JPX" if ext == '.jpx' else "PY"
        print(f"  [{lang}] {name:20s} ({rel_path})")

    print(f"\nTotal: {len(modules)} modules")

    print("\nSearch paths (priority order):")
    for i, p in enumerate(interp.import_handler.get_search_paths(), 1):
        exists = "✓" if os.path.isdir(p) else "✗"
        print(f"  {i}. {exists} {p}")


def main():
    """Main entry point"""
    # Setup argument parser
    parser = argparse.ArgumentParser(
        description="JPX Programming Language Interpreter",
        add_help=False  # Kita handle help sendiri
    )

    parser.add_argument('file', nargs='?', help='JPX script file to run')
    parser.add_argument('-v', '--version', action='store_true', help='Show version')
    parser.add_argument('-h', '--help', action='store_true', help='Show help')
    parser.add_argument('--info', action='store_true', help='Show system information')
    parser.add_argument('--list-modules', action='store_true',
                        help='List all available modules')

    args = parser.parse_args()

    # Handle commands
    if args.version:
        show_version()
    elif args.help:
        show_help()
    elif args.info:
        show_info()
    elif args.list_modules:
        list_modules()
    elif args.file:
        run_file(args.file)
    else:
        # No arguments
        show_help()
        sys.exit(1)

if __name__ == '__main__':
    main()