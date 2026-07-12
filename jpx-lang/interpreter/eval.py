# eval.py - JPX Expression Evaluator
# Version: 2.1.0 Stable
# Professional release with ternary operator and full expression support

import re
import json
from . import exceptions
from .function import JPXFunction, JPXReturnException

class EvalHandler:
    """JPX Expression Evaluator - Handles all expression evaluation"""
    
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.cache = {}

    # ================== STRING INTERPOLATION ==================
    def process_string(self, s):
        """Handle $variable inside strings"""
        def repl_var(match):
            var_path = match.group(1)
            try:
                value = self.interpreter.get_value(var_path)
                return str(value) if value is not None else ""
            except exceptions.JPXNameError:
                return f"<undefined:{var_path}>"
            except Exception as e:
                return f"<error:{e}>"
        
        pattern = r'\$([a-zA-Z_][a-zA-Z0-9_.]*)'
        return re.sub(pattern, repl_var, s)

    def is_identifier(self, s):
        """Check if string is a valid identifier"""
        if not s:
            return False
        return bool(re.match(r'^[a-zA-Z_][a-zA-Z0-9_.]*$', s))

    # ================== STRING METHODS ==================

    def _call_string_method(self, s, method_name, args):
        """Panggil method string native. Return None kalau method tidak
        dikenal (agar fall through ke path lain).

        Method yang didukung (mirip Python str methods):
          s.split(sep=None)         -> list of strings
          s.strip()                 -> trimmed string
          s.lstrip()                -> trimmed left
          s.rstrip()                -> trimmed right
          s.replace(old, new)       -> replaced string
          s.upper()                 -> uppercase
          s.lower()                 -> lowercase
          s.contains(sub)           -> bool
          s.startsWith(prefix)      -> bool
          s.endsWith(suffix)        -> bool
          s.find(sub)               -> int (index or -1)
          s.count(sub)              -> int
          s.repeat(n)               -> string repeated n times
          s.substring(start, end)   -> slice
          s.toCharArray()           -> list of chars
        """
        try:
            if method_name == 'split':
                if not args:
                    return s.split()
                return s.split(args[0])
            if method_name == 'strip':
                return s.strip()
            if method_name == 'lstrip':
                return s.lstrip()
            if method_name == 'rstrip':
                return s.rstrip()
            if method_name == 'replace':
                if len(args) >= 2:
                    return s.replace(str(args[0]), str(args[1]))
                return s
            if method_name == 'upper':
                return s.upper()
            if method_name == 'lower':
                return s.lower()
            if method_name == 'contains':
                return str(args[0]) in s
            if method_name == 'startsWith':
                return s.startswith(str(args[0]))
            if method_name == 'endsWith':
                return s.endswith(str(args[0]))
            if method_name == 'find':
                return s.find(str(args[0]))
            if method_name == 'count':
                return s.count(str(args[0]))
            if method_name == 'repeat':
                return s * int(args[0])
            if method_name == 'substring':
                if len(args) == 1:
                    return s[int(args[0]):]
                elif len(args) == 2:
                    return s[int(args[0]):int(args[1])]
                return s
            if method_name == 'toCharArray':
                return list(s)
            # Method tidak dikenal — return None agar fall through
            return None
        except (IndexError, TypeError, ValueError) as e:
            raise exceptions.JPXTypeError(
                f"Error calling string method '{method_name}': {e}"
            )

    # ================== CLASS SUPPORT ==================

    def _instantiate_class(self, cls, args):
        """Buat instance baru dari class.

        Instance = dict dengan struktur:
          '__class__'  : reference ke class dict
          'fields'     : dict untuk instance fields (mutable)

        Constructor __init__ dipanggil dengan `self` sebagai argumen pertama.
        Di dalam __init__, `self.field = value` men-set field di instance.
        """
        instance = {
            '__class__': cls,
            'fields': {}
        }
        if cls['init'] is not None:
            cls['init'].call([instance] + args)
        return instance

    # ================== ASSIGNMENT HELPERS ==================

    def _find_assignment_eq(self, expr):
        """Cari posisi `=` yang merupakan assignment (bukan `==`, `!=`,
        `<=`, `>=`, `+=`, dll). Hanya `=` tunggal yang valid. Track
        parenthesis/bracket/brace depth dan string state.
        Return posisi `=` atau -1 kalau tidak ketemu.
        """
        in_string = False
        quote_char = None
        depth = 0
        i = 0
        while i < len(expr):
            ch = expr[i]
            if in_string:
                if ch == '\\':
                    i += 2
                    continue
                if ch == quote_char:
                    in_string = False
                i += 1
                continue
            if ch in '"\'':
                in_string = True
                quote_char = ch
                i += 1
                continue
            if ch in '([{':
                depth += 1
            elif ch in ')]}':
                depth -= 1
            elif ch == '=' and depth == 0:
                # Cek char sebelum dan sesudah
                prev = expr[i-1] if i > 0 else ''
                nxt = expr[i+1] if i+1 < len(expr) else ''
                if prev in '!<>=' or nxt == '=':
                    # Bukan assignment (==, !=, <=, >=, +=, -=, dll)
                    i += 1
                    continue
                return i
            i += 1
        return -1

    def _split_top_commas(self, expr):
        """Split expr by commas yang ada di top-level (depth=0, not in string)."""
        parts = []
        current = []
        in_string = False
        quote_char = None
        depth = 0
        i = 0
        while i < len(expr):
            ch = expr[i]
            if in_string:
                if ch == '\\':
                    current.append(ch)
                    if i + 1 < len(expr):
                        current.append(expr[i+1])
                    i += 2
                    continue
                current.append(ch)
                if ch == quote_char:
                    in_string = False
                i += 1
                continue
            if ch in '"\'':
                in_string = True
                quote_char = ch
                current.append(ch)
                i += 1
                continue
            if ch in '([{':
                depth += 1
                current.append(ch)
            elif ch in ')]}':
                depth -= 1
                current.append(ch)
            elif ch == ',' and depth == 0:
                parts.append(''.join(current))
                current = []
            else:
                current.append(ch)
            i += 1
        if current:
            parts.append(''.join(current))
        return parts

    def _assign_to(self, target, value):
        """Assign value ke target. Target bisa:
        - IDENT sederhana:     `x`
        - Index access:        `arr[i]`, `matrix[i][j]`
        - Property access:     `obj.field`
        """
        target = target.strip()

        # Index access: IDENT[idx] (atau chained IDENT[idx1][idx2])
        if '[' in target and target.endswith(']'):
            # Parse IDENT awal dan rangkaian [idx]
            m = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)', target)
            if not m:
                raise exceptions.JPXSyntaxError(f"Invalid assignment target: {target!r}")
            obj = self.interpreter.get_value(m.group(1))
            pos = m.end()

            # Loop baca [idx] sampai terakhir
            indices = []
            while pos < len(target):
                if target[pos] != '[':
                    break
                # Cari matching ]
                depth = 1
                end = pos + 1
                while end < len(target) and depth > 0:
                    if target[end] == '[':
                        depth += 1
                    elif target[end] == ']':
                        depth -= 1
                        if depth == 0:
                            break
                    end += 1
                inner = target[pos+1:end].strip()
                if ':' in inner and not inner.startswith('"'):
                    # Slice — gak support assignment ke slice (TODO nanti)
                    raise exceptions.JPXSyntaxError(
                        f"Cannot assign to slice: {target!r}"
                    )
                # Evaluasi index
                if (inner.startswith('"') and inner.endswith('"')) or \
                   (inner.startswith("'") and inner.endswith("'")):
                    idx = inner[1:-1]
                else:
                    idx_val = self.eval_expression(inner)
                    if isinstance(idx_val, str) and idx_val.isdigit():
                        idx = int(idx_val)
                    elif isinstance(idx_val, (int, float)) and not isinstance(idx_val, bool):
                        idx = int(idx_val)
                    else:
                        idx = idx_val
                indices.append(idx)
                pos = end + 1

            # Traverse semua index kecuali terakhir, lalu set yang terakhir
            for idx in indices[:-1]:
                obj = obj[idx]
            obj[indices[-1]] = value
            return

        # Property access: IDENT.field (set attribute di JPX module/object/instance)
        if '.' in target:
            parts = target.split('.')
            if len(parts) == 2:
                obj_name = parts[0].strip()
                prop = parts[1].strip()
                try:
                    obj = self.interpreter.get_value(obj_name)
                except exceptions.JPXNameError:
                    raise exceptions.JPXNameError(f"Undefined variable: {obj_name}")
                # Class instance — set field
                if isinstance(obj, dict) and '__class__' in obj:
                    obj['fields'][prop] = value
                    return
                # Dict biasa
                if isinstance(obj, dict):
                    obj[prop] = value
                    return
                # Object Python biasa
                setattr(obj, prop, value)
                return
            raise exceptions.JPXSyntaxError(
                f"Nested property assignment not supported: {target!r}"
            )

        # IDENT sederhana
        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', target):
            self.interpreter.env[target] = value
            self.cache[target] = value
            return

        raise exceptions.JPXSyntaxError(f"Invalid assignment target: {target!r}")

    # ================== TRUTHINESS ==================
    def is_truthy(self, val):
        """Check if value is truthy for conditions"""
        if val is None:
            return False
        if isinstance(val, bool):
            return val
        if isinstance(val, (int, float)):
            return val != 0
        if isinstance(val, str):
            return val != ""
        if isinstance(val, (list, tuple, dict)):
            return len(val) > 0
        return True

    # ================== TERNARY OPERATOR ==================
    def _eval_ternary(self, expr):
        """Evaluate ternary operator: condition ? true_val : false_val"""
        # Find position of '?' not inside quotes or brackets
        in_string = False
        paren_depth = 0
        bracket_depth = 0
        brace_depth = 0
        question_pos = -1
        
        for i, ch in enumerate(expr):
            if ch == '"':
                in_string = not in_string
            elif not in_string:
                if ch == '(':
                    paren_depth += 1
                elif ch == ')':
                    paren_depth -= 1
                elif ch == '[':
                    bracket_depth += 1
                elif ch == ']':
                    bracket_depth -= 1
                elif ch == '{':
                    brace_depth += 1
                elif ch == '}':
                    brace_depth -= 1
                elif ch == '?' and paren_depth == 0 and bracket_depth == 0 and brace_depth == 0:
                    question_pos = i
                    break
        
        if question_pos == -1:
            return None
        
        condition = expr[:question_pos].strip()
        rest = expr[question_pos+1:].strip()
        
        # Find matching ':'
        in_string = False
        paren_depth = 0
        bracket_depth = 0
        brace_depth = 0
        colon_pos = -1
        
        for i, ch in enumerate(rest):
            if ch == '"':
                in_string = not in_string
            elif not in_string:
                if ch == '(':
                    paren_depth += 1
                elif ch == ')':
                    paren_depth -= 1
                elif ch == '[':
                    bracket_depth += 1
                elif ch == ']':
                    bracket_depth -= 1
                elif ch == '{':
                    brace_depth += 1
                elif ch == '}':
                    brace_depth -= 1
                elif ch == ':' and paren_depth == 0 and bracket_depth == 0 and brace_depth == 0:
                    colon_pos = i
                    break
        
        if colon_pos == -1:
            raise exceptions.JPXSyntaxError(f"Invalid ternary: missing ':'")
        
        true_val = rest[:colon_pos].strip()
        false_val = rest[colon_pos+1:].strip()
        
        # Evaluate condition
        cond_result = self.eval_expression(condition)
        
        if self.is_truthy(cond_result):
            return self.eval_expression(true_val)
        else:
            return self.eval_expression(false_val)

    # ================== ARGUMENT PARSING ==================
    def parse_args(self, args_str):
        """Parse function arguments"""
        if not args_str:
            return []
        
        args = []
        current = []
        depth = 0
        in_string = False
        escape = False
        
        i = 0
        while i < len(args_str):
            ch = args_str[i]
            
            if in_string:
                current.append(ch)
                if ch == '"' and not escape:
                    in_string = False
                elif ch == '\\' and not escape:
                    escape = True
                else:
                    escape = False
                i += 1
                continue
            
            if ch == '"':
                in_string = True
                current.append(ch)
                i += 1
                continue
            
            if ch in '([{':
                depth += 1
                current.append(ch)
                i += 1
                continue
                
            if ch in ')]}':
                depth -= 1
                current.append(ch)
                i += 1
                continue
            
            if ch == ',' and depth == 0 and not in_string:
                arg = ''.join(current).strip()
                if arg:
                    args.append(self.eval_expression(arg))
                current = []
                i += 1
                continue
            
            current.append(ch)
            i += 1
        
        if current:
            arg = ''.join(current).strip()
            if arg:
                args.append(self.eval_expression(arg))
        
        return args

    # ================== LIST PARSING ==================
    def _parse_list(self, expr):
        """Parse list literal [1, 2, 3]"""
        inner = expr[1:-1].strip()
        if not inner:
            return []
        
        items = []
        current = []
        depth = 0
        in_string = False
        escape = False
        
        i = 0
        while i < len(inner):
            ch = inner[i]
            
            if in_string:
                current.append(ch)
                if ch == '"' and not escape:
                    in_string = False
                elif ch == '\\' and not escape:
                    escape = True
                else:
                    escape = False
                i += 1
                continue
            
            if ch == '"':
                in_string = True
                current.append(ch)
                i += 1
                continue
            
            if ch in '([{':
                depth += 1
                current.append(ch)
                i += 1
                continue
                
            if ch in ')]}':
                depth -= 1
                current.append(ch)
                i += 1
                continue
            
            if ch == ',' and depth == 0 and not in_string:
                item = ''.join(current).strip()
                if item:
                    items.append(self.eval_expression(item))
                current = []
                i += 1
                continue
            
            current.append(ch)
            i += 1
        
        if current:
            item = ''.join(current).strip()
            if item:
                items.append(self.eval_expression(item))
        
        return items

    # ================== OBJECT PARSING ==================
    def _parse_object(self, expr):
        """Parse object literal {key: value}"""
        inner = expr[1:-1].strip()
        if not inner:
            return {}
        
        obj = {}
        current_key = []
        current_val = []
        state = 'key'
        depth = 0
        in_string = False
        escape = False
        
        i = 0
        while i < len(inner):
            ch = inner[i]
            
            if in_string:
                if state == 'key':
                    current_key.append(ch)
                else:
                    current_val.append(ch)
                    
                if ch == '"' and not escape:
                    in_string = False
                elif ch == '\\' and not escape:
                    escape = True
                else:
                    escape = False
                i += 1
                continue
            
            if ch == '"':
                in_string = True
                if state == 'key':
                    current_key.append(ch)
                else:
                    current_val.append(ch)
                i += 1
                continue
            
            if ch in '([{':
                depth += 1
                if state == 'key':
                    current_key.append(ch)
                else:
                    current_val.append(ch)
                i += 1
                continue
                
            if ch in ')]}':
                depth -= 1
                if state == 'key':
                    current_key.append(ch)
                else:
                    current_val.append(ch)
                i += 1
                continue
            
            if ch == ':' and depth == 0 and not in_string and state == 'key':
                state = 'val'
                i += 1
                continue
            
            if ch == ',' and depth == 0 and not in_string and state == 'val':
                key = ''.join(current_key).strip()
                val = ''.join(current_val).strip()
                if key:
                    if key.startswith('"') and key.endswith('"'):
                        key = key[1:-1]
                    if val:
                        obj[key] = self.eval_expression(val)
                    else:
                        obj[key] = None
                current_key = []
                current_val = []
                state = 'key'
                i += 1
                continue
            
            if state == 'key':
                current_key.append(ch)
            else:
                current_val.append(ch)
            i += 1
        
        if current_key:
            key = ''.join(current_key).strip()
            val = ''.join(current_val).strip()
            if key:
                if key.startswith('"') and key.endswith('"'):
                    key = key[1:-1]
                if val:
                    obj[key] = self.eval_expression(val)
                else:
                    obj[key] = None
        
        return obj

    # ================== OPERATOR FINDER ==================
    def find_operator(self, expr, ops):
        """Find operator position from right (precedence)"""
        if not expr:
            return -1, None

        in_string = False
        depth = 0
        # NOTE: sebelumnya ada `bracket_depth` dan `brace_depth` yang di-update
        # di branch `elif ch == '[' / ']' / '{' / '}'`, tapi branch tersebut
        # tidak pernah tercapai karena `ch in '([{'` sudah menangani `[` `{`.
        # Akibatnya kedua variabel selalu 0 — dead code. Sekarang kita
        # mengandalkan `depth` saja (yang mencakup () [] {} sekaligus).

        for i in range(len(expr)-1, -1, -1):
            ch = expr[i]

            if ch == '"':
                in_string = not in_string
            elif ch in '([{':
                depth -= 1
            elif ch in ')]}':
                depth += 1
            elif not in_string and depth == 0:
                for op in ops:
                    op_len = len(op)
                    if i - op_len + 1 >= 0 and expr[i-op_len+1:i+1] == op:
                        if op == '-' and (i-op_len+1 == 0 or
                            (i-op_len >= 0 and expr[i-op_len] in '+-*/([{=, ')):
                            continue
                        return i - op_len + 1, op
        return -1, None

    # ================== PATH NAVIGATION ==================
    def get_value_by_path(self, path):
        """Get value from dot notation path"""
        parts = path.split('.')
        
        # Handle array access like data[1].name
        if '[' in parts[0] and ']' in parts[0]:
            array_match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\[(.+?)\]$', parts[0])
            if array_match:
                array_name = array_match.group(1)
                index_expr = array_match.group(2).strip()
                
                obj = self.interpreter.get_value(array_name)
                if obj is None:
                    return None
                
                try:
                    if index_expr.isdigit():
                        index = int(index_expr)
                    else:
                        index_val = self.eval_expression(index_expr)
                        if isinstance(index_val, str) and index_val.isdigit():
                            index = int(index_val)
                        else:
                            index = index_val
                    
                    current = obj[index]
                except (IndexError, KeyError, TypeError):
                    return None
                
                for part in parts[1:]:
                    if current is None:
                        return None
                    if isinstance(current, dict):
                        current = current.get(part)
                    elif isinstance(current, (list, tuple)) and part.isdigit():
                        try:
                            current = current[int(part)]
                        except (IndexError, ValueError):
                            return None
                    else:
                        try:
                            current = getattr(current, part)
                        except AttributeError:
                            return None
                return current
        
        # Regular dot notation
        obj = self.interpreter.get_value(parts[0])
        if obj is None:
            return None
        
        current = obj
        for part in parts[1:]:
            if current is None:
                return None
            if isinstance(current, dict):
                current = current.get(part)
            elif isinstance(current, (list, tuple)) and part.isdigit():
                try:
                    current = current[int(part)]
                except (IndexError, ValueError):
                    return None
            else:
                try:
                    current = getattr(current, part)
                except AttributeError:
                    return None
        return current

    # ================== MAIN EVALUATOR ==================
    def eval_expression(self, expr):
        """Evaluate a JPX expression"""
        expr = expr.strip()
        if not expr:
            return None

        # String literal: hanya jika expr adalah SATU string literal utuh,
        # bukan rangkaian seperti `"a" + "b"` (yang juga mulai dan berakhir
        # dengan `"`). Sebelumnya check hanya `startswith('"') and endswith('"')`
        # sehingga `"a" + "b"` salah dianggap satu string berisi `a" + "b`.
        if expr.startswith('"') and expr.endswith('"') and len(expr) >= 2:
            # Scan dari awal, lewati escape, dan cek apakah closing quote
            # pertama jatuh tepat di akhir expr.
            j = 1
            closed = False
            while j < len(expr):
                if expr[j] == '\\' and j + 1 < len(expr):
                    j += 2
                    continue
                if expr[j] == '"':
                    if j == len(expr) - 1:
                        closed = True
                    break
                j += 1
            if closed:
                return self.process_string(expr[1:-1])

        if expr.startswith('"""') and expr.endswith('"""') and len(expr) >= 6:
            # Triple-quoted string — cek tidak ada `"""` lain di tengah.
            inner = expr[3:-3]
            if '"""' not in inner:
                return self.process_string(inner)

        # Ternary operator
        if '?' in expr and ':' in expr:
            ternary_result = self._eval_ternary(expr)
            if ternary_result is not None:
                return ternary_result

        # Cache lookup
        if expr in self.cache and expr not in self.interpreter.env:
            return self.cache[expr]

        # Break/continue
        if expr in ('break', 'broke'):
            raise exceptions.JPXBreakException()
        if expr == 'continue':
            raise exceptions.JPXContinueException()

        # Print statement
        # Sebelumnya punya blok khusus untuk `print a + b` yang selalu
        # memperlakukan `+` sebagai string concat, sehingga `print 3 + 4`
        # menghasilkan "34". Sekarang kita delegasikan evaluasi ke
        # `eval_expression` yang sudah menangani `+` numerik vs string
        # dengan benar.
        if expr.startswith('print '):
            content = expr[6:].strip()
            value = self.eval_expression(content)
            if value is not None:
                print(value)
            return None

        # String methods native — cek SEBELUM function call path, karena
        # `s.contains(...)` juga match function call regex `IDENT.attr(...)`.
        # Method yang didukung: split, strip, replace, upper, lower, contains,
        # startsWith, endsWith, find, count, repeat, substring, toCharArray.
        # Syntax: IDENT.method(args) atau "literal".method(args)
        string_method_match = re.match(
            r'^([a-zA-Z_][a-zA-Z0-9_]*|"[^"]*"|\'[^\']*\')\s*\.\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*)\)\s*$',
            expr, re.DOTALL
        )
        if string_method_match:
            obj_str = string_method_match.group(1)
            method_name = string_method_match.group(2)
            args_str = string_method_match.group(3)

            # Evaluasi objek
            if obj_str.startswith('"') and obj_str.endswith('"'):
                obj = self.process_string(obj_str[1:-1])
            elif obj_str.startswith("'") and obj_str.endswith("'"):
                obj = obj_str[1:-1]
            else:
                try:
                    obj = self.interpreter.get_value(obj_str)
                except exceptions.JPXNameError:
                    obj = None

            if isinstance(obj, str):
                args = self.parse_args(args_str)
                result = self._call_string_method(obj, method_name, args)
                if result is not None:
                    return result
            # Kalau bukan string atau method tidak dikenal, fall through ke
            # function call / chained access path

        # Function call: IDENT(args)
        # Sebelumnya pakai regex greedy `^IDENT\((.*)\)$` yang menelan
        # `len(kata[i]) > len(longest)` sebagai function call `len(...)`
        # karena `(` pertama dan `)` terakhir cocok, padahal bukan pasangan.
        # Sekarang kita cek manual: `(` pertama dan `)` terakhir HARUS pasangan
        # matching (depth balanced di antaranya hanya pada akhir).
        func_match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_.]*)\s*\(', expr)
        if func_match:
            func_path = func_match.group(1)
            open_pos = expr.find('(', func_match.end() - 1)
            # Cek apakah `)` terakhir adalah matching paren dari `(` pertama
            depth = 0
            matching_close = -1
            for i in range(open_pos, len(expr)):
                if expr[i] == '(':
                    depth += 1
                elif expr[i] == ')':
                    depth -= 1
                    if depth == 0:
                        matching_close = i
                        break
            if matching_close == len(expr) - 1 and matching_close > open_pos:
                args_str = expr[open_pos + 1:matching_close]
                args = self.parse_args(args_str)

                try:
                    if '.' in func_path:
                        # Method call: instance.method(args) atau
                        # module.func(args) atau class.method(args)
                        # atau instance.field.method(args) (chained)
                        parts = func_path.split('.')
                        obj = self.interpreter.get_value(parts[0])

                        # Traverse semua parts kecuali terakhir
                        # Mendukung instance.field.method() dan instance.method()
                        for i in range(1, len(parts) - 1):
                            part = parts[i]
                            if isinstance(obj, dict) and '__class__' in obj:
                                # Instance — cek fields dulu, lalu methods
                                if part in obj['fields']:
                                    obj = obj['fields'][part]
                                elif part in obj['__class__']['methods']:
                                    obj = obj['__class__']['methods'][part]
                                else:
                                    raise exceptions.JPXAttributeError(
                                        f"Instance has no attribute '{part}'"
                                    )
                            elif isinstance(obj, dict):
                                obj = obj.get(part)
                            else:
                                obj = getattr(obj, part, None)

                        # Part terakhir = method/attr yang akan dipanggil
                        last_part = parts[-1]

                        # Cek apakah ini adalah instance method call
                        if isinstance(obj, dict) and '__class__' in obj:
                            cls = obj['__class__']
                            if last_part in cls['methods']:
                                method = cls['methods'][last_part]
                                # Inject `self` ke args
                                return method.call([obj] + args)
                            elif last_part == '__init__':
                                return obj  # already initialized
                            # Mungkin field yang berupa function/JPXFunction
                            if last_part in obj['fields']:
                                fn = obj['fields'][last_part]
                                if callable(fn):
                                    if isinstance(fn, JPXFunction):
                                        return fn.call(args)
                                    return fn(*args)
                                return fn
                            raise exceptions.JPXTypeError(
                                f"Method '{last_part}' not found in class '{cls['name']}'"
                            )

                        # Bukan instance — handle sebagai property/method biasa
                        if isinstance(obj, dict):
                            fn = obj.get(last_part)
                        else:
                            fn = getattr(obj, last_part, None)
                        if callable(fn):
                            if isinstance(fn, JPXFunction):
                                return fn.call(args)
                            return fn(*args)
                        return fn
                    else:
                        # Simple function call atau class instantiation
                        func = self.interpreter.get_value(func_path)
                        if func is not None:
                            # Cek apakah ini class (dict dengan __jpx_class__)
                            if isinstance(func, dict) and func.get('__jpx_class__'):
                                return self._instantiate_class(func, args)
                            if callable(func):
                                if isinstance(func, JPXFunction):
                                    return func.call(args)
                                return func(*args)
                            return func
                except exceptions.JPXError:
                    raise
                except Exception as e:
                    raise exceptions.JPXTypeError(f"Error calling {func_path}: {str(e)}")

        # Assignment: deteksi `target = value`.
        # Target bisa:
        #   - IDENT sederhana:        `x = 5`
        #   - Index access:           `arr[i] = value`  (mutable list)
        #   - Nested index access:    `matrix[i][j] = value`
        #   - Property access:        `obj.field = value`
        #   - Multiple assignment:    `a, b = x, y`     (dipisah oleh koma di LHS)
        #
        # Regex sebelumnya hanya handle IDENT sederhana. Sekarang kita
        # parse manual: cari `=` yang valid (bukan `==`, `!=`, `<=`, `>=`),
        # lalu lihat target-nya.
        if not expr.startswith(('if ', 'while ', 'for ', 'try ', 'function ')):
            # Cari `=` yang valid (single, bukan comparison) di top-level
            eq_pos = self._find_assignment_eq(expr)
            if eq_pos > 0:
                target = expr[:eq_pos].strip()
                value_str = expr[eq_pos+1:].strip()

                # Multiple assignment: `a, b = x, y`
                if ',' in target and not target.startswith('['):
                    # Split LHS dan RHS by comma (di top-level)
                    lhs_parts = self._split_top_commas(target)
                    rhs_parts = self._split_top_commas(value_str)
                    if len(lhs_parts) == len(rhs_parts):
                        # Eval semua RHS dulu sebelum assign, agar swap
                        # seperti `x, y = y, x` bekerja dengan benar.
                        values = [self.eval_expression(rt.strip()) for rt in rhs_parts]
                        for lt, val in zip(lhs_parts, values):
                            self._assign_to(lt.strip(), val)
                        return None

                # Single assignment
                value = self.eval_expression(value_str)
                self._assign_to(target, value)
                return value

        # Parentheses: hanya jika outer paren adalah pasangan matching.
        # Sebelumnya hanya cek `startswith('(') and endswith(')')`, yang
        # menelan `(4 * 6) / f(2, 3)` — paren awal dan akhir BUKAN pasangan,
        # sehingga `expr[1:-1]` = `4 * 6) / f(2, 3` → error.
        if expr.startswith('(') and expr.endswith(')'):
            depth = 0
            matched = True
            for i, ch in enumerate(expr):
                if ch == '(':
                    depth += 1
                elif ch == ')':
                    depth -= 1
                    if depth == 0 and i != len(expr) - 1:
                        # Closing paren before end → outer parens not matched
                        matched = False
                        break
            if matched and depth == 0:
                return self.eval_expression(expr[1:-1].strip())

        # Object literal
        if expr.startswith('{') and expr.endswith('}'):
            return self._parse_object(expr)

        # List literal
        if expr.startswith('[') and expr.endswith(']'):
            return self._parse_list(expr)

        # Generalized chained index/slice/property access.
        # Sebelumnya pakai 3 regex terpisah (nested_match, slice_match,
        # index_match) yang masing-masing hanya handle 1-2 level akses dan
        # gak support variable index di nested (mis. `tokens[p][0]`).
        # Sekarang parse manual: ambil IDENT awal, lalu loop baca suffix
        # `[...]` (index/slice) atau `.key` (property) satu per satu.
        #
        # PENTING: setelah loop selesai, kita cek bahwa seluruh expr sudah
        # dikonsumsi. Kalau masih ada sisa (mis. `tok[0] == "NUM"` punya
        # sisa ` == "NUM"`), berarti ini BUKAN pure access — biarkan path
        # lain (comparison/addition) yang handle.
        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_.]*\s*\[', expr) or \
           re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\s*\.\s*[a-zA-Z_]', expr):
            m = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)', expr)
            try:
                obj = self.interpreter.get_value(m.group(1))
            except exceptions.JPXNameError:
                obj = None
            if obj is None:
                # Mungkin literal float seperti `3.7` — cek dulu
                rest = expr[m.end():].strip()
                if rest and rest[0] == '.':
                    possible_num = m.group(1) + rest
                    try:
                        if '.' in possible_num and possible_num.replace('.', '', 1).isdigit():
                            return float(possible_num)
                    except ValueError:
                        pass
                raise exceptions.JPXNameError(f"Undefined variable: {m.group(1)}")

            pos = m.end()
            consumed_all = False
            while pos < len(expr):
                # Skip whitespace
                while pos < len(expr) and expr[pos] == ' ':
                    pos += 1
                if pos >= len(expr):
                    consumed_all = True
                    break
                if expr[pos] == '.':
                    pm = re.match(r'\s*\.\s*([a-zA-Z_][a-zA-Z0-9_]*)', expr[pos:])
                    if not pm:
                        break
                    prop_name = pm.group(1)
                    # Class instance — baca dari fields dict
                    if isinstance(obj, dict) and '__class__' in obj:
                        if prop_name in obj['fields']:
                            obj = obj['fields'][prop_name]
                        elif prop_name in obj['__class__']['methods']:
                            # Akses method tanpa panggil — return bound method?
                            # Untuk sekarang, return method function sendiri
                            obj = obj['__class__']['methods'][prop_name]
                        else:
                            raise exceptions.JPXAttributeError(
                                f"Instance has no attribute '{prop_name}'"
                            )
                    # Dict biasa
                    elif isinstance(obj, dict):
                        obj = obj.get(prop_name)
                    # Module / object Python
                    else:
                        try:
                            obj = getattr(obj, prop_name)
                        except AttributeError:
                            return obj
                    pos += pm.end()
                elif expr[pos] == '[':
                    depth = 1
                    end = pos + 1
                    while end < len(expr) and depth > 0:
                        if expr[end] == '[':
                            depth += 1
                        elif expr[end] == ']':
                            depth -= 1
                            if depth == 0:
                                break
                        end += 1
                    if depth != 0:
                        break
                    inner = expr[pos+1:end].strip()
                    if ':' in inner and not inner.startswith('"') and not inner.startswith("'"):
                        parts = inner.split(':', 1)
                        start_s = parts[0].strip()
                        end_s = parts[1].strip()
                        start = self.eval_expression(start_s) if start_s else None
                        end_v = self.eval_expression(end_s) if end_s else None
                        try:
                            obj = obj[start:end_v]
                        except TypeError:
                            raise exceptions.JPXTypeError(f"Cannot slice {type(obj).__name__}")
                    else:
                        if (inner.startswith('"') and inner.endswith('"')) or \
                           (inner.startswith("'") and inner.endswith("'")):
                            idx = inner[1:-1]
                        else:
                            idx_val = self.eval_expression(inner)
                            if isinstance(idx_val, str) and idx_val.isdigit():
                                idx = int(idx_val)
                            elif isinstance(idx_val, (int, float)) and not isinstance(idx_val, bool):
                                idx = int(idx_val)
                            else:
                                idx = idx_val
                        try:
                            obj = obj[idx]
                        except (IndexError, KeyError, TypeError) as e:
                            raise exceptions.JPXTypeError(
                                f"Cannot index {type(obj).__name__} with {idx!r}: {e}"
                            )
                    pos = end + 1
                else:
                    # Char bukan `.` atau `[` — berarti ada operator setelah
                    # access (mis. `tok[0] == "NUM"`). Bukan pure access,
                    # break dan biarkan path lain handle.
                    break

            # Hanya return kalau seluruh expr habis dikonsumsi
            if pos >= len(expr):
                return obj
            # Kalau gak habis, fall through ke path lain (comparison, dll)

        # Number literal (float) — cek SEBELUM property access agar `3.7`
        # tidak salah dianggap sebagai akses property `3.7` (var `3` .
        # property `7`). Sebelumnya blok ini ada di paling bawah, sehingga
        # property access lebih dulu menangkap literal float.
        try:
            if expr.isdigit():
                return int(expr)
            if expr.replace('.', '', 1).isdigit() and expr.count('.') == 1:
                return float(expr)
            if expr.startswith('-') and expr[1:].replace('.', '', 1).isdigit():
                return float(expr)
        except:
            pass

        # Property access
        # Hanya jika parts[0] adalah identifier valid (bukan angka).
        if '.' in expr and not expr.endswith(' length'):
            first_part = expr.split('.', 1)[0]
            if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', first_part):
                val = self.get_value_by_path(expr)
                if val is not None:
                    return val

        # Length operator
        if expr.endswith(' length'):
            var_name = expr[:-7].strip()
            val = self.interpreter.get_value(var_name)
            if val is None:
                raise exceptions.JPXNameError(f"Undefined variable: {var_name}")
            if isinstance(val, (list, tuple, dict, str)):
                return len(val)
            raise exceptions.JPXTypeError(f"Cannot get length of {type(val).__name__}")

        # Logical operators
        if ' and ' in expr:
            parts = expr.split(' and ')
            for part in parts:
                if not self.eval_expression(part.strip()):
                    return False
            return True
            
        if ' or ' in expr:
            parts = expr.split(' or ')
            for part in parts:
                if self.eval_expression(part.strip()):
                    return True
            return False
            
        if expr.startswith('not '):
            return not self.eval_expression(expr[4:].strip())

        # Comparison operators
        # Track parenthesis depth agar operator di dalam (...) tidak di-split.
        # Sebelumnya `"x: " + (5 == 5)` di-split di `==` yang ada di dalam
        # paren → left=`"x: " + (5` right=`5)` → error.
        for op in ['<=', '>=', '==', '!=', '<', '>']:
            if op not in expr:
                continue
            in_string = False
            depth = 0
            for i in range(len(expr) - len(op) + 1):
                ch = expr[i]
                if ch == '"':
                    in_string = not in_string
                elif not in_string:
                    if ch in '([{':
                        depth += 1
                    elif ch in ')]}':
                        depth -= 1
                    elif depth == 0 and expr[i:i+len(op)] == op:
                        left = expr[:i].strip()
                        right = expr[i+len(op):].strip()
                        left_val = self.eval_expression(left)
                        right_val = self.eval_expression(right)

                        try:
                            if op == '==': return left_val == right_val
                            if op == '!=': return left_val != right_val
                            if op == '<': return left_val < right_val
                            if op == '>': return left_val > right_val
                            if op == '<=': return left_val <= right_val
                            if op == '>=': return left_val >= right_val
                        except TypeError:
                            raise exceptions.JPXTypeError(
                                f"Cannot compare {type(left_val).__name__} and {type(right_val).__name__}"
                            )
                        break

        # Addition / String concatenation
        # Sebelumnya blok ini selalu menggabungkan operand sebagai string,
        # sehingga `3 + 4` menghasilkan "34" bukan 7. Sekarang kita evaluasi
        # semua operand dulu, lalu pilih mode (numerik vs string) berdasarkan
        # tipe operand.
        if '+' in expr:
            parts = []
            current = []
            depth = 0
            in_string = False

            for ch in expr:
                if ch == '"':
                    in_string = not in_string
                    current.append(ch)
                elif in_string:
                    current.append(ch)
                elif ch == '+' and depth == 0:
                    parts.append(''.join(current).strip())
                    current = []
                elif ch in '([{':
                    depth += 1
                    current.append(ch)
                elif ch in ')]}':
                    depth -= 1
                    current.append(ch)
                else:
                    current.append(ch)

            if current:
                parts.append(''.join(current).strip())

            if len(parts) > 1:
                # Evaluasi semua operand sekali
                values = []
                for part in parts:
                    if part.startswith('"') and part.endswith('"'):
                        values.append(self.process_string(part[1:-1]))
                    else:
                        values.append(self.eval_expression(part))

                # Mode list concat: semua operand adalah list
                all_list = all(isinstance(v, list) for v in values if v is not None)
                if all_list and any(isinstance(v, list) for v in values):
                    result = []
                    for v in values:
                        if v is None:
                            continue
                        result = result + v
                    return result

                # Mode numerik: semua operand adalah int/float (atau None yang
                # kita perlakukan sebagai 0 hanya jika semua operand numerik).
                all_numeric = all(
                    v is None or isinstance(v, (int, float)) and not isinstance(v, bool)
                    for v in values
                )
                if all_numeric:
                    total = 0
                    for v in values:
                        if v is None:
                            continue
                        total += v
                    return total

                # Mode string: minimal satu operand adalah str (atau ada bool,
                # list, dict — kita konsolidasi ke str)
                result = ""
                for v in values:
                    if v is None:
                        continue
                    result += str(v)
                return result

        # Subtraction
        # Subtraction: track depth agar `-` di dalam (...) atau [...] tidak
        # di-split. Sebelumnya `(arr[n / 2 - 1] + ...)` di-split di `-` yang
        # ada di dalam `[...]`, menghasilkan left=`(arr[n / 2 ` → invalid.
        if '-' in expr and not expr.startswith('-'):
            in_string = False
            depth = 0
            for i in range(len(expr)-1, -1, -1):
                ch = expr[i]
                if ch == '"':
                    in_string = not in_string
                elif not in_string:
                    if ch in ')]}':
                        depth += 1
                    elif ch in '([{':
                        depth -= 1
                    elif ch == '-' and depth == 0:
                        if i == 0:
                            continue
                        # Treat `-` as unary (skip) only if the previous
                        # non-space char is an operator/bracket.
                        prev = i - 1
                        while prev >= 0 and expr[prev] == ' ':
                            prev -= 1
                        if prev >= 0 and expr[prev] in '+-*/([{=,':
                            continue

                        left = expr[:i].strip()
                        right = expr[i+1:].strip()

                        if left and right:
                            left_val = self.eval_expression(left)
                            right_val = self.eval_expression(right)

                            if left_val is not None and right_val is not None:
                                try:
                                    return float(left_val) - float(right_val)
                                except (ValueError, TypeError):
                                    pass
                        break

        # Multiplication, Division, Integer Division & Modulo
        # Support: * / // %   (// = integer division, return int)
        # Track parenthesis depth agar operator di dalam (...) tidak di-split.
        # Scan dari kanan, cek `//` sebelum `/` agar tidak salah split.
        if '*' in expr or '/' in expr or '%' in expr:
            in_string = False
            depth = 0
            i = len(expr) - 1
            while i >= 0:
                ch = expr[i]
                if ch == '"':
                    in_string = not in_string
                elif not in_string:
                    if ch in ')]}':
                        depth += 1
                    elif ch in '([{':
                        depth -= 1
                    elif depth == 0:
                        # Cek `//` (2 char) lebih dulu
                        if i > 0 and expr[i] == '/' and expr[i-1] == '/':
                            left = expr[:i-1].strip()
                            right = expr[i+1:].strip()
                            if left and right:
                                left_val = self.eval_expression(left)
                                right_val = self.eval_expression(right)
                                if left_val is None: left_val = 0
                                if right_val is None: right_val = 0
                                try:
                                    r = float(right_val)
                                    if r == 0:
                                        raise exceptions.JPXTypeError("Integer division by zero")
                                    return int(float(left_val) // r)
                                except (ValueError, TypeError):
                                    pass
                            break
                            i -= 1
                            continue
                        if ch in '*/%' and not (ch == '/' and i > 0 and expr[i-1] == '/'):
                            left = expr[:i].strip()
                            right = expr[i+1:].strip()
                            if left and right:
                                left_val = self.eval_expression(left)
                                right_val = self.eval_expression(right)
                                if left_val is None: left_val = 0
                                if right_val is None: right_val = 0
                                try:
                                    l = float(left_val)
                                    r = float(right_val)
                                    if ch == '*':
                                        # Preserve int jika kedua operand int
                                        if isinstance(left_val, int) and isinstance(right_val, int):
                                            return int(left_val) * int(right_val)
                                        return l * r
                                    elif ch == '/':
                                        if r == 0:
                                            raise exceptions.JPXTypeError("Division by zero")
                                        return l / r
                                    else:  # %
                                        if r == 0:
                                            raise exceptions.JPXTypeError("Modulo by zero")
                                        if isinstance(left_val, int) and isinstance(right_val, int):
                                            return int(left_val) % int(right_val)
                                        return l - (int(l / r) * r)
                                except (ValueError, TypeError):
                                    pass
                            break
                i -= 1

        # Unary minus
        if expr.startswith('-'):
            rest = expr[1:].strip()
            if rest:
                val = self.eval_expression(rest)
                if val is None:
                    return 0
                try:
                    return -float(val)
                except (ValueError, TypeError):
                    return -val if isinstance(val, (int, float)) else val

        # Numbers
        try:
            if expr.isdigit():
                return int(expr)
            if expr.replace('.', '', 1).isdigit() and expr.count('.') == 1:
                return float(expr)
            if expr.startswith('-') and expr[1:].replace('.', '', 1).isdigit():
                return float(expr)
        except:
            pass

        # Boolean & Null
        if expr == 'true': return True
        if expr == 'false': return False
        if expr == 'null': return None

        # Variable lookup
        if self.is_identifier(expr):
            try:
                return self.interpreter.get_value(expr)
            except exceptions.JPXNameError:
                raise exceptions.JPXNameError(
                    f"Variable '{expr}' not defined. Use 'global [{expr} = value]' to declare it."
                )

        raise exceptions.JPXSyntaxError(f"Invalid expression: '{expr}'")