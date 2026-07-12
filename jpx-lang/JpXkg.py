#!/usr/bin/env python3
# jpxkg.py - JPX Package Installer v1.0
# Usage: jpxkg install <package> or jpxkg -v

import os
import sys
import json
import hashlib
import urllib.request
import urllib.error
import shutil
import argparse

VERSION = "1.0.0"
ROOT = os.path.dirname(os.path.abspath(__file__))
LIB_DIR = os.path.join(ROOT, "lib")
INDEX_PATH = os.path.join(ROOT, "index.json")

def ensure_lib():
    os.makedirs(LIB_DIR, exist_ok=True)

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def load_index():
    if not os.path.exists(INDEX_PATH):
        print(f"❌ index.json not found in {ROOT}")
        return None
    try:
        with open(INDEX_PATH, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to load index.json: {e}")
        return None

def install(pkg_name):
    ensure_lib()
    idx = load_index()
    if not idx:
        return False

    pkg = next((m for m in idx.get("modules", []) if m["name"] == pkg_name), None)
    if not pkg:
        print(f"❌ Package '{pkg_name}' not found in index")
        available = [m["name"] for m in idx.get("modules", [])]
        if available:
            print(f"📦 Available: {', '.join(available)}")
        return False

    url = pkg.get("download_url")
    if not url:
        print(f"❌ No download URL for {pkg_name}")
        return False

    dest = os.path.join(ROOT, pkg.get("install_path", f"lib/{pkg_name}.py"))
    os.makedirs(os.path.dirname(dest), exist_ok=True)

    if os.path.exists(dest):
        print(f"⚠️ {dest} already exists")
        if input("Overwrite? [y/N] ").lower() not in ("y", "yes"):
            print("📦 Installation cancelled")
            return False

    tmp = dest + ".tmp"
    print(f"📦 Downloading {pkg_name}...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "JPX-Installer/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            total = int(resp.headers.get("Content-Length", 0))
            with open(tmp, "wb") as f:
                dl = 0
                while True:
                    chunk = resp.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
                    dl += len(chunk)
                    if total:
                        pct = dl * 100 // total
                        print(f"  Progress: {pct}%", end="\r")
        print()
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return False

    exp_sha = pkg.get("sha256")
    if exp_sha:
        print("  Verifying SHA256...")
        actual = sha256_file(tmp)
        if actual != exp_sha:
            print(f"❌ SHA256 mismatch")
            print(f"  Expected: {exp_sha}")
            print(f"  Actual:   {actual}")
            if input("Continue anyway? [y/N] ").lower() not in ("y", "yes"):
                os.remove(tmp)
                return False
            print("⚠️ Continuing with mismatched checksum")
        else:
            print("✅ SHA256 OK")

    shutil.move(tmp, dest)
    size = os.path.getsize(dest)
    size_str = f"{size/1024:.1f} KB" if size < 1024*1024 else f"{size/(1024*1024):.1f} MB"
    print(f"✅ Installed {pkg_name} to {pkg.get('install_path')} ({size_str})")

    deps = pkg.get("dependencies", [])
    if deps:
        print("⚠️ Dependencies:")
        for d in deps:
            print(f"  • {d} (pip install {d})")
    return True

def main():
    # Custom argument parser untuk handle -v tanpa command
    if len(sys.argv) == 1:
        print("JPX Package Manager v1.0")
        print("Usage: jpxkg install <package>")
        print("       jpxkg -v, --version")
        return
        
    if len(sys.argv) == 2 and sys.argv[1] in ("-v", "--version"):
        print(f"jpxkg version {VERSION}")
        return
    
    if len(sys.argv) < 2:
        print("❌ Missing command")
        print("Usage: jpxkg install <package>")
        return
    
    command = sys.argv[1]
    
    if command != "install":
        print(f"❌ Unknown command: {command}")
        print("Usage: jpxkg install <package>")
        return
    
    if len(sys.argv) < 3:
        print("❌ Please specify a package")
        print("Usage: jpxkg install <package>")
        return
    
    package = sys.argv[2]
    install(package)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted")
        sys.exit(130)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)