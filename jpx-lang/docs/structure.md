# JPX Project Structure (Modular)

Struktur direktori JPX setelah refactoring Phase B.

## Directory Layout

```
jpx/
├── jpx.py                          # CLI entry point (Python)
├── jpxkg.py                        # Package manager (Python)
├── LICENSE.txt
├── README.md
│
├── core/                           # Interpreter core (Python)
│   ├── __init__.py
│   ├── exceptions/                 # Exception module (package)
│   │   ├── __init__.py             # Re-exports semua exceptions
│   │   ├── base.py                 # JPXError, JPXExceptionWrapper
│   │   ├── syntax.py               # JPXSyntaxError
│   │   ├── name.py                 # JPXNameError
│   │   ├── type.py                 # JPXTypeError
│   │   ├── attribute.py            # JPXAttributeError
│   │   ├── runtime.py              # JPXRuntimeError, JPXImportError
│   │   └── control.py              # break/continue/return exceptions
│   ├── lexer/                      # (future: lexer subsystem)
│   ├── parser/                     # (future: parser subsystem)
│   └── runtime/                    # (future: runtime subsystem)
│
├── interpreter/                    # ⚠️ DEPRECATED - pindah ke core/
│   ├── __init__.py
│   ├── interpreter.py              # Main interpreter loop
│   ├── eval.py                     # Expression evaluator
│   ├── function.py                 # JPXFunction class
│   ├── importer.py                 # Module loader (v4.0)
│   ├── lexer.py                    # Tokenizer (new)
│   ├── parser.py                   # Recursive descent parser (new)
│   ├── astnodes.py                 # AST node definitions (new)
│   └── exceptions.py               # Re-export dari core/exceptions/
│
├── stdlib/                         # Standard library (target structure)
│   ├── text/                       # String/text modules
│   │   ├── string.py
│   │   ├── color.py
│   │   └── beuty.py
│   ├── math/                       # Math modules
│   │   ├── math.py
│   │   ├── random.py
│   │   └── mathx.jpx
│   ├── io/                         # I/O modules
│   │   ├── print.py
│   │   ├── scanner.py
│   │   ├── fs.py
│   │   └── env.py
│   ├── net/                        # Network modules
│   │   ├── requests.py
│   │   └── speedreq.py
│   ├── os/                         # OS-specific modules
│   │   ├── system.py
│   │   ├── time.py
│   │   ├── notification.py
│   │   ├── subnotif.py
│   │   ├── win32sys.py
│   │   ├── win32ui.py
│   │   ├── JpXUi.py
│   │   └── mem.py
│   ├── system/                     # System-level modules
│   │   ├── hash.py
│   │   ├── JpXhash.py
│   │   └── ReGx.py
│   └── collections/                # Collection types
│       ├── array.jpx
│       └── json.py
│
├── library/                        # ⚠️ Backward compat - symlink to stdlib/
│   └── (files still here for compat)
│
├── lib/                            # User-installed packages (jpxkg install)
│
├── tests/
│   ├── unit/                       # Unit tests
│   │   ├── test_lexer_parser.py
│   │   ├── test_new_features.py
│   │   ├── test_phase_a.jpx
│   │   ├── self_test.jpx
│   │   ├── test_array_lib.jpx
│   │   └── test_mathx_lib.jpx
│   ├── e2e/                        # End-to-end tests
│   │   └── test_showcase.jpx
│   └── run_tests.py                # Test runner
│
├── examples/                       # Example JPX programs
│   ├── demo_lib.jpx
│   ├── demo_string.jpx
│   ├── demo_game.jpx
│   ├── mini_interp.jpx             # Mini interpreter written in JPX!
│   ├── test_native_import.jpx
│   └── multi_module/               # Multi-module demo
│       ├── main.jpx
│       ├── utils.jpx
│       └── validator.jpx
│
├── docs/                           # Documentation
│   ├── structure.md                # This file
│   ├── syntax.md                   # (future) Syntax reference
│   └── roadmap.md                  # (future) Development roadmap
│
└── spec/                           # Language specification
    ├── grammar.ebnf                # (future) BNF grammar
    └── ast.md                      # (future) AST spec
```

## Modularity Principles

1. **Satu class per file** di `core/exceptions/` — memudahkan maintenance
2. **Subdomain grouping** di `stdlib/` — text, math, io, net, os, system, collections
3. **Backward compatibility** — `interpreter/exceptions.py` re-export dari `core/exceptions/`
4. **Self-hosted modules** (`*.jpx`) hidup berdampingan dengan native (`.py`)

## Import Patterns

### Internal Python imports
```python
# OLD (still works)
from .exceptions import JPXSyntaxError

# NEW (preferred)
from core.exceptions import JPXSyntaxError
# atau lebih spesifik:
from core.exceptions.syntax import JPXSyntaxError
```

### JPX user imports
```jpx
[string];      # import dari stdlib/text/string.py
[array];       # import dari stdlib/collections/array.jpx
[myhelper];    # import dari script dir atau lib/
```

## Migration Status

| Component | Old Location | New Location | Status |
|-----------|--------------|--------------|--------|
| Exceptions | `interpreter/exceptions.py` | `core/exceptions/` | ✅ Done |
| Lexer | `interpreter/lexer.py` | `core/lexer/` | ⏳ Pending |
| Parser | `interpreter/parser.py` | `core/parser/` | ⏳ Pending |
| Runtime | `interpreter/interpreter.py` + `eval.py` | `core/runtime/` | ⏳ Pending |
| Stdlib | `library/` | `stdlib/{text,math,io,...}/` | ⏳ Pending |
