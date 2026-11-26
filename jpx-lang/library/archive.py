# library/archive.py — JPX native archive module
# Exposes `archive` for [archive]; imports. Handles every format shogun
# can meet in the wild: zip · tar · tar.gz/tgz · tar.bz2/tbz2 · tar.xz/txz
# · single gz/bz2 · tar.zst/tzst/zst.
#
# zip + all tar variants are pure Python stdlib. zstd is NOT in the
# stdlib — .zst falls back to the system `zstd` binary, with a clear
# install hint when it is missing.
#
# Security: zip-slip guard on every member (zip has NO '..' protection
# in stdlib; tar uses tarfile's data filter on py3.12+). Every result
# dict always carries all keys (ok · format · files · error) — JPX
# raises on missing dict keys.
import os
import zipfile
import tarfile
import gzip
import bz2
import shutil
import subprocess


def _sniff_format(path):
    """Content sniffing fallback when the extension says nothing.
    Magic bytes: PK zip · gzip · bzip2 · xz · zstd · tar probe."""
    try:
        with open(path, 'rb') as f:
            head = f.read(8)
        if head[:4] == b'PK\x03\x04' or head[:4] == b'PK\x05\x06':
            return 'zip'
        if head[:2] == b'\x1f\x8b':
            return 'gz'
        if head[:3] == b'BZh':
            return 'bz2'
        if head[:6] == b'\xfd7zXZ\x00':
            return 'tar.xz'
        if head[:4] == b'\x28\xb5\x2f\xfd':
            return 'zst'
        try:
            with tarfile.open(path, 'r:') as t:
                first = next(iter(t), None)
                return 'tar' if first is not None else ''
        except Exception:
            return ''
    except Exception:
        return ''


def _detect_format(path):
    """Format from extension; unknown extension → sniff magic bytes."""
    fmt = _ext_format(path)
    if fmt == '':
        fmt = _sniff_format(path)
    return fmt


def _ext_format(path):
    """Format from extension (lowercase, both separators normalized)."""
    n = os.path.basename(path).lower()
    if n.endswith(('.tar.zst', '.tzst')):
        return 'tar.zst'
    if n.endswith('.tar.gz') or n.endswith('.tgz'):
        return 'tar.gz'
    if n.endswith('.tar.bz2') or n.endswith('.tbz2'):
        return 'tar.bz2'
    if n.endswith('.tar.xz') or n.endswith('.txz'):
        return 'tar.xz'
    if n.endswith('.tar'):
        return 'tar'
    if n.endswith('.zip'):
        return 'zip'
    if n.endswith('.gz'):
        return 'gz'
    if n.endswith('.bz2'):
        return 'bz2'
    if n.endswith('.zst'):
        return 'zst'
    return ''


def _safe_zip_name(name):
    """True when a zip member cannot escape the destination.
    Checks both separators (archives built on windows use backslashes),
    absolute paths, drive letters and '..' components."""
    n = name.replace('\\', '/')
    if n.startswith('/') or (len(n) > 1 and n[1] == ':'):
        return False
    for part in n.split('/'):
        if part in ('..', ''):
            if part == '..':
                return False
        # empty parts from '//' or trailing '/' are harmless
    return True


def _extract_zip(path, dest):
    files = 0
    with zipfile.ZipFile(path) as z:
        for zi in z.infolist():
            if not _safe_zip_name(zi.filename):
                raise ValueError('unsafe zip member rejected: ' + zi.filename)
        for zi in z.infolist():
            target = os.path.join(dest, zi.filename.replace('\\', '/'))
            if zi.filename.endswith(('/', '\\')) or zi.is_dir():
                os.makedirs(target, exist_ok=True)
                continue
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with z.open(zi) as src, open(target, 'wb') as out:
                shutil.copyfileobj(src, out)
            mode = (zi.external_attr >> 16) & 0o777
            if mode & 0o111:
                os.chmod(target, mode | 0o444)
            files += 1
    return files


def _extract_tar(path, dest, fmt):
    mode_map = {'tar': 'r:', 'tar.gz': 'r:gz', 'tar.bz2': 'r:bz2', 'tar.xz': 'r:xz'}
    files = 0
    with tarfile.open(path, mode_map[fmt]) as t:
        try:
            t.extractall(dest, filter='data')  # py3.12+: zip-slip safe
        except TypeError:
            t.extractall(dest)                 # older python fallback
        for m in t.getmembers():
            if m.isfile():
                files += 1
    return files


def _extract_single_gz(path, dest):
    out = os.path.join(dest, os.path.basename(path)[:-3])
    with gzip.open(path, 'rb') as src, open(out, 'wb') as dst:
        shutil.copyfileobj(src, dst)
    os.chmod(out, 0o755)
    return 1


def _extract_single_bz2(path, dest):
    out = os.path.join(dest, os.path.basename(path)[:-4])
    with bz2.open(path, 'rb') as src, open(out, 'wb') as dst:
        shutil.copyfileobj(src, dst)
    os.chmod(out, 0o755)
    return 1


def _zstd_binary():
    return shutil.which('zstd')


def _extract_zst(path, dest):
    """tar.zst/tzst → zstd | tar ; single zst → plain decompression.
    Needs the system zstd binary (not in python stdlib)."""
    z = _zstd_binary()
    if not z:
        raise RuntimeError(
            'zstd binary not found — install it first: '
            'apt install zstd / dnf install zstd / pacman -S zstd / '
            'winget install Facebook.Zstd')
    fmt = _detect_format(path)
    if fmt == 'tar.zst':
        p = subprocess.run(
            [z, '-d', '-c', path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=600)
        if p.returncode != 0:
            raise RuntimeError('zstd decompress failed: ' + p.stderr.decode(errors='replace')[:200])
        import io
        with tarfile.open(fileobj=io.BytesIO(p.stdout), mode='r:') as t:
            try:
                t.extractall(dest, filter='data')
            except TypeError:
                t.extractall(dest)
            return sum(1 for m in t.getmembers() if m.isfile())
    out = os.path.join(dest, os.path.basename(path)[:-4] or 'decompressed')
    p = subprocess.run([z, '-d', '-f', '-o', out, path],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=600)
    if p.returncode != 0:
        raise RuntimeError('zstd decompress failed: ' + p.stderr.decode(errors='replace')[:200])
    os.chmod(out, 0o755)
    return 1


class Archive:
    """Archive extraction for JPX — usage:
        [archive];
        global [res = archive.extract("/tmp/pkg.zip", "/tmp/out")];
        res["ok"] · res["format"] · res["files"] · res["error"]"""

    def supported(self, path):
        """True when the extension is a format this module handles."""
        return _detect_format(str(path)) != ''

    def format(self, path):
        """Format name from the extension: zip / tar / tar.gz / tar.bz2 /
        tar.xz / gz / bz2 / zst / tar.zst · empty string = unknown."""
        return _detect_format(str(path))

    def members(self, path):
        """List member filenames without extracting (zip + tar only).
        Returns [] for single-file formats or on error."""
        fmt = _detect_format(str(path))
        try:
            if fmt == 'zip':
                with zipfile.ZipFile(path) as z:
                    return [zi.filename for zi in z.infolist()]
            if fmt in ('tar', 'tar.gz', 'tar.bz2', 'tar.xz'):
                mode_map = {'tar': 'r:', 'tar.gz': 'r:gz',
                            'tar.bz2': 'r:bz2', 'tar.xz': 'r:xz'}
                with tarfile.open(path, mode_map[fmt]) as t:
                    return [m.name for m in t.getmembers()]
        except Exception:
            return []
        return []

    def extract(self, path, dest):
        """Extract archive `path` into directory `dest` (created if needed).
        Returns {ok, format, files, error} — ok=false carries a readable
        error; unsafe members are rejected, never written."""
        path = str(path)
        dest = str(dest)
        res = {'ok': False, 'format': '', 'files': 0, 'error': ''}
        if not os.path.exists(path):
            res['error'] = 'archive not found: ' + path
            return res
        fmt = _detect_format(path)
        res['format'] = fmt
        if fmt == '':
            res['error'] = ('unsupported archive format: ' +
                            os.path.basename(path))
            return res
        try:
            os.makedirs(dest, exist_ok=True)
            if fmt == 'zip':
                res['files'] = _extract_zip(path, dest)
            elif fmt in ('tar', 'tar.gz', 'tar.bz2', 'tar.xz'):
                res['files'] = _extract_tar(path, dest, fmt)
            elif fmt == 'gz':
                res['files'] = _extract_single_gz(path, dest)
            elif fmt == 'bz2':
                res['files'] = _extract_single_bz2(path, dest)
            elif fmt in ('zst', 'tar.zst'):
                res['files'] = _extract_zst(path, dest)
            res['ok'] = True
        except Exception as e:
            res['error'] = str(e)
        return res


exports = {'archive': Archive()}
