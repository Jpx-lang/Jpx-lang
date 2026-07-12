# importer.py - JPX Module Import Handler
# Version: 4.0.0
#
# Memuat modul dari beberapa search path:
#   1. Directory script yang sedang dijalankan (relative import)
#   2. Built-in library/ (di root JPX)
#   3. User lib/ (di current working directory)
#   4. Directory tambahan dari JPX_PATH env var
#
# Support dua format file:
#   - .py  : modul native Python (lebih cepat, akses penuh ke Python stdlib)
#   - .jpx : modul self-hosted (ditulis dalam JPX sendiri)
#
# Syntax import yang didukung:
#   [module]                    # import seluruh module
#   [module.attr]               # import atribut spesifik dari module
#   [a, b, c]                   # import multiple modules sekaligus
#   [module.attr1, module.attr2] # multiple attributes

import os
import sys
import importlib.util
from . import exceptions


class ImportHandler:
    """JPX Module Import Handler."""

    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.module_cache = {}

        # Determine base paths
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            self.base_path = os.path.dirname(sys.executable)
        else:
            # Running as script
            self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Current working directory for user modules
        self.cwd = os.getcwd()

        # Built-in library path (di root JPX)
        self.builtin_path = os.path.join(self.base_path, 'library')

        # User library path (di current directory)
        self.user_path = os.path.join(self.cwd, 'lib')

        # Script directory — di-set oleh jpx.py saat menjalankan file.
        # Memungkinkan `import [helper]` untuk memuat helper.jpx dari
        # direktori yang sama dengan script utama.
        self.script_dir = None

        # Additional search paths dari JPX_PATH env var
        # Format: JPX_PATH="/path/1:/path/2" (pakai os.pathsep)
        self.extra_paths = []
        jpx_path = os.environ.get('JPX_PATH', '')
        if jpx_path:
            for p in jpx_path.split(os.pathsep):
                p = p.strip()
                if p and os.path.isdir(p):
                    self.extra_paths.append(p)

        # Stack modul yang sedang di-load — untuk deteksi circular import.
        # Kalau modul A import B dan B import A, kita kasih error jelas
        # alih-alih infinite loop.
        self._loading_stack = []

        # Ensure built-in directories exist (jangan create user_path otomatis
        # karena bisa surprise user dengan folder lib/ di cwd).
        os.makedirs(self.builtin_path, exist_ok=True)

    # ============================================================
    # PUBLIC API
    # ============================================================

    def set_script_dir(self, path):
        """Set directory dari script yang sedang dijalankan. Dipanggil
        oleh jpx.py saat mulai. Memungkinkan relative import."""
        if path and os.path.isdir(path):
            self.script_dir = os.path.abspath(path)

    def add_search_path(self, path):
        """Tambah search path baru secara programatik."""
        if path and os.path.isdir(path):
            abs_path = os.path.abspath(path)
            if abs_path not in self.extra_paths:
                self.extra_paths.append(abs_path)

    def get_search_paths(self):
        """Return list semua search path yang aktif (urutan = prioritas)."""
        paths = []
        # 1. Script directory (paling prioritas — relative import)
        if self.script_dir:
            paths.append(self.script_dir)
        # 2. User lib/ (cwd)
        paths.append(self.user_path)
        # 3. Extra paths (JPX_PATH)
        paths.extend(self.extra_paths)
        # 4. Built-in library/ (terakhir — fallback)
        paths.append(self.builtin_path)
        return paths

    # ============================================================
    # MODULE FINDING
    # ============================================================

    def find_module(self, module_name):
        """Cari module di semua search path. Return (path, lang) atau None.

        Urutan pencarian:
          1. Folder package: path/module_name/  (hanya jika ada _jpx_.jpx)
             → load _jpx_.jpx sebagai package init
          2. script_dir/module_name.jpx
          3. script_dir/module_name.py
          4. lib/module_name.jpx
          5. lib/module_name.py
          6. JPX_PATH entries (jpx lalu py, lalu folder package)
          7. library/module_name.jpx (built-in)
          8. library/module_name.py

        .jpx diprioritaskan di script_dir dan lib/ (user code),
        .py diprioritaskan di library/ (native).

        Folder packages: direktori yang berisi file `_jpx_.jpx` dianggap
        sebagai package yang bisa di-import. File `_jpx_.jpx` berfungsi
        seperti `__init__.py` di Python — dieksekusi saat package di-import.
        """
        searched = []
        for path in self.get_search_paths():
            is_builtin = (path == self.builtin_path)

            # 1. Cek folder package: path/module_name/ dengan _jpx_.jpx
            pkg_dir = os.path.join(path, module_name)
            if os.path.isdir(pkg_dir):
                init_jpx = os.path.join(pkg_dir, '_jpx_.jpx')
                init_py = os.path.join(pkg_dir, '_jpx_.py')
                if os.path.isfile(init_jpx):
                    return (init_jpx, 'jpx')
                if os.path.isfile(init_py):
                    return (init_py, 'py')

            # 2. Cek file module
            if is_builtin:
                candidates = [
                    (module_name + '.py', 'py'),
                    (module_name + '.jpx', 'jpx'),
                ]
            else:
                candidates = [
                    (module_name + '.jpx', 'jpx'),
                    (module_name + '.py', 'py'),
                ]

            for filename, lang in candidates:
                full = os.path.join(path, filename)
                if os.path.isfile(full):
                    return (full, lang)
                searched.append(full)

        return None

    def _format_search_paths(self):
        """Format search paths untuk error message."""
        return '\n  - '.join(self.get_search_paths())

    # ============================================================
    # MODULE LOADING
    # ============================================================

    def load_module(self, module_name):
        """Load module by name. Return module object atau None kalau
        tidak ketemu. Raise JPXImportError kalau ada masalah."""
        # Cek cache dulu
        if module_name in self.module_cache:
            return self.module_cache[module_name]

        # Deteksi circular import
        if module_name in self._loading_stack:
            chain = ' -> '.join(self._loading_stack + [module_name])
            raise exceptions.JPXImportError(
                f"Circular import detected: {chain}\n"
                f"Module '{module_name}' is being loaded but tries to "
                f"import itself (directly or indirectly)."
            )

        # Cari file
        result = self.find_module(module_name)
        if result is None:
            return None

        module_path, lang = result

        # Tandai sedang loading
        self._loading_stack.append(module_name)
        try:
            if lang == 'py':
                module = self._load_python_module(module_name, module_path)
            else:
                module = self._load_jpx_module(module_name, module_path)
            self.module_cache[module_name] = module
            return module
        finally:
            self._loading_stack.pop()

    def _load_python_module(self, module_name, module_path):
        """Load file .py sebagai Python module via importlib."""
        try:
            # Pakai unique name agar tidak konflik dengan sys.modules
            spec_name = f'_jpx_{module_name}'
            spec = importlib.util.spec_from_file_location(spec_name, module_path)
            if spec is None:
                raise exceptions.JPXImportError(
                    f"Failed to create spec for {module_name}"
                )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        except exceptions.JPXImportError:
            raise
        except Exception as e:
            raise exceptions.JPXImportError(
                f"Failed to load Python module '{module_name}' "
                f"from {module_path}: {e}"
            )

    def _load_jpx_module(self, module_name, module_path):
        """Jalankan file .jpx sebagai module. Semua top-level function dan
        global variable di-expose sebagai exports.

        Penting:
        - Kita simpan state interpreter utama, lalu jalankan module code
          di environment bersih (closure env kosong).
        - Module code gak punya akses ke variabel script utama — modul
          harus self-contained.
        - Setelah selesai, exports = semua function + global var yang
          didefinisikan di top-level.
        """
        try:
            with open(module_path, 'r', encoding='utf-8-sig') as f:
                code = f.read()
        except Exception as e:
            raise exceptions.JPXImportError(
                f"Cannot read JPX module '{module_name}' "
                f"from {module_path}: {e}"
            )

        # Simpan state interpreter utama
        old_env = self.interpreter.env
        old_functions = self.interpreter.functions
        old_return = self.interpreter.return_value
        old_loop = self.interpreter.loop_depth
        old_builtins = self.interpreter.builtins

        # Environment baru khusus untuk module
        # Builtins tetap di-share agar module bisa pakai int(), str(), dll.
        self.interpreter.env = {}
        self.interpreter.functions = {}
        self.interpreter.return_value = None
        self.interpreter.loop_depth = 0

        try:
            self.interpreter.run(code)
        except Exception as e:
            # Restore dulu sebelum raise
            self.interpreter.env = old_env
            self.interpreter.functions = old_functions
            self.interpreter.return_value = old_return
            self.interpreter.loop_depth = old_loop
            self.interpreter.builtins = old_builtins
            raise exceptions.JPXImportError(
                f"Error executing JPX module '{module_name}' "
                f"({module_path}): {e}"
            )

        # Tangkap exports
        exports = {}
        exports.update(self.interpreter.env)
        exports.update(self.interpreter.functions)

        # Late binding fix-up: setelah semua function di-defined, update
        # closure_env setiap JPXFunction agar include semua sibling functions.
        # Sebelumnya, function A yang di-define sebelum function B tidak
        # bisa call B karena B belum ada di closure snapshot A. Sekarang
        # kita inject semua exports ke setiap function's closure_env.
        from .function import JPXFunction
        for key, value in exports.items():
            if isinstance(value, JPXFunction):
                # Merge exports ke closure_env (tapi jangan override params)
                for k, v in exports.items():
                    if k not in value.closure_env:
                        value.closure_env[k] = v

        # Restore interpreter state
        self.interpreter.env = old_env
        self.interpreter.functions = old_functions
        self.interpreter.return_value = old_return
        self.interpreter.loop_depth = old_loop
        self.interpreter.builtins = old_builtins

        # Buat module object
        class JPXModule:
            """Lightweight wrapper untuk module yang ditulis dalam JPX."""
            def __repr__(self):
                return f"<JPXModule '{module_name}'>"

        mod = JPXModule()
        mod.exports = exports
        mod.__jpx__ = True
        mod.__name__ = module_name
        mod.__file__ = module_path
        for k, v in exports.items():
            setattr(mod, k, v)
        return mod

    # ============================================================
    # IMPORT STATEMENT HANDLING
    # ============================================================

    def handle(self, stmt):
        """Handle import statement.

        Syntax yang didukung:
          [module]                      — import seluruh module
          [module.attr]                 — import satu atribut
          [a, b, c]                     — import multiple modules
          [m.a, m.b, n.c]               — multiple attributes from multiple modules
        """
        # Strip brackets
        inner = stmt[1:-1].strip()

        # Split by comma untuk multi-import
        # Tapi hati-hati: jangan split kalau comma ada di dalam string.
        # Untuk sekarang, kita asumsikan module name tidak ada comma.
        if ',' in inner:
            parts = [p.strip() for p in inner.split(',') if p.strip()]
            for part in parts:
                self._import_one(part)
        else:
            self._import_one(inner)

    def _import_one(self, name):
        """Import satu module atau atribut.

        Support:
          [module]           — import module
          [module.attr]      — import attribute dari module
          [pkg.submodule]    — import sub-module dari package folder
                              (cari pkg/submodule.jpx atau pkg/submodule.py)
        """
        # Handle module.attr atau pkg.submodule
        if '.' in name:
            parts = name.split('.')
            if len(parts) != 2:
                raise exceptions.JPXImportError(
                    f"Invalid import '{name}': only 'module.attr' "
                    f"or 'pkg.submodule' syntax is supported"
                )
            module_name = parts[0].strip()
            attr_name = parts[1].strip()

            # Coba load parent module dulu
            module = self.load_module(module_name)

            # === SUB-MODULE CHECK ===
            # Kalau parent module adalah package (folder), cek apakah
            # attr_name adalah sub-module file di dalam folder tersebut.
            # Contoh: [jpx.string] → cari jpx/string.jpx di search paths
            if module is not None and getattr(module, '__jpx__', False):
                # module adalah .jpx package — cek __file__ untuk dapat folder
                pkg_file = getattr(module, '__file__', None)
                if pkg_file:
                    pkg_dir = os.path.dirname(pkg_file)
                    # Cari sub-module di folder package
                    for ext in ('.jpx', '.py'):
                        sub_file = os.path.join(pkg_dir, attr_name + ext)
                        if os.path.isfile(sub_file):
                            # Load sub-module
                            lang = 'jpx' if ext == '.jpx' else 'py'
                            if lang == 'jpx':
                                sub_mod = self._load_jpx_module(attr_name, sub_file)
                            else:
                                sub_mod = self._load_python_module(attr_name, sub_file)
                            # Expose sebagai attr_name
                            if getattr(sub_mod, '__jpx__', False):
                                self.interpreter.builtins[attr_name] = sub_mod
                                self.interpreter.env[attr_name] = sub_mod
                            elif hasattr(sub_mod, 'exports') and isinstance(sub_mod.exports, dict):
                                for k, v in sub_mod.exports.items():
                                    self.interpreter.builtins[k] = v
                                    self.interpreter.env[k] = v
                            return

            # === ATTRIBUTE CHECK ===
            # Bukan sub-module — cek sebagai attribute biasa
            if module is None:
                raise exceptions.JPXImportError(
                    f"Module '{module_name}' not found.\n"
                    f"Searched in:\n  - {self._format_search_paths()}"
                )

            # Cek exports dict dulu
            value = None
            found = False
            if hasattr(module, 'exports') and isinstance(module.exports, dict):
                if attr_name in module.exports:
                    value = module.exports[attr_name]
                    found = True

            # Kalau gak ada di exports, cek attribute langsung
            if not found and hasattr(module, attr_name):
                value = getattr(module, attr_name)
                found = True

            if not found:
                # List available attributes untuk bantu debugging
                available = []
                if hasattr(module, 'exports') and isinstance(module.exports, dict):
                    available = list(module.exports.keys())
                elif hasattr(module, '__jpx__'):
                    available = [k for k in dir(module)
                                 if not k.startswith('_') and k not in ('exports',)]
                raise exceptions.JPXImportError(
                    f"Attribute '{attr_name}' not found in module '{module_name}'.\n"
                    f"Available: {', '.join(sorted(available))}"
                )

            self.interpreter.builtins[attr_name] = value
            self.interpreter.env[attr_name] = value
            return

        # Simple module import
        module = self.load_module(name)
        if module is None:
            raise exceptions.JPXImportError(
                f"Module '{name}' not found.\n"
                f"Searched in:\n  - {self._format_search_paths()}"
            )

        # Untuk .jpx module, expose module object itu sendiri dengan namanya
        # agar user bisa akses `array.first(...)`, `mathx.fib(...)`, dst.
        if getattr(module, '__jpx__', False):
            self.interpreter.builtins[name] = module
            self.interpreter.env[name] = module
            return

        # Untuk .py module dengan pattern `exports = {...}` (existing pattern
        # dari color.py, string.py, dll), expose setiap key individually.
        if hasattr(module, 'exports') and isinstance(module.exports, dict):
            for key, value in module.exports.items():
                self.interpreter.builtins[key] = value
                self.interpreter.env[key] = value
            return

        # Fallback: expose semua attribute non-private
        for attr_name in dir(module):
            if attr_name.startswith('_'):
                continue
            attr = getattr(module, attr_name)
            if callable(attr) or isinstance(attr, (str, int, float, bool, dict, list)):
                self.interpreter.builtins[attr_name] = attr
                self.interpreter.env[attr_name] = attr

    # ============================================================
    # UTILITIES
    # ============================================================

    def list_available_modules(self):
        """List semua module yang tersedia di search paths (untuk debugging
        dan untuk `jpx --list-modules`).

        Mendeteksi:
          - File modules: module.jpx, module.py
          - Folder packages: module/ dengan _jpx_.jpx atau _jpx_.py
        """
        seen = {}
        for path in self.get_search_paths():
            if not os.path.isdir(path):
                continue
            for entry in os.listdir(path):
                full = os.path.join(path, entry)

                # Folder package: cek _jpx_.jpx atau _jpx_.py
                if os.path.isdir(full):
                    init_jpx = os.path.join(full, '_jpx_.jpx')
                    init_py = os.path.join(full, '_jpx_.py')
                    if os.path.isfile(init_jpx):
                        if entry not in seen:
                            seen[entry] = ('.jpx (package)', init_jpx)
                    elif os.path.isfile(init_py):
                        if entry not in seen:
                            seen[entry] = ('.py (package)', init_py)
                    continue

                # File module
                name, ext = os.path.splitext(entry)
                if ext in ('.py', '.jpx') and name not in seen:
                    if name != '_jpx_':  # skip _jpx_ files (they're package inits)
                        seen[name] = (ext, full)
        return seen

    def clear_cache(self):
        """Clear module cache. Berguna untuk hot-reload di REPL."""
        self.module_cache.clear()
