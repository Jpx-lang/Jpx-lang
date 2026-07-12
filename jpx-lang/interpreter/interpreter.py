# interpreter.py - JPX Language Interpreter
# Version: 2.1.0 Stable
# Professional release with try-catch error handling

import re
import sys
from . import importer
from .eval import EvalHandler
from .function import JPXFunction, JPXReturnException
from . import exceptions

class JPXInterpreter:
    """JPX Language Interpreter - Core execution engine"""
    
    def __init__(self):
        self.env = {}
        # Built-in functions and constants.
        # Sebelumnya hanya `true`/`false`/`null`. Sekarang tambah:
        #   int(x)        - convert to int
        #   float(x)      - convert to float
        #   str(x)        - convert to string
        #   bool(x)       - convert to bool
        #   len(x)        - length of str/list/dict
        #   ord(s)        - char code of first char
        #   chr(n)        - char from code
        #   type(x)       - type name string
        self.builtins = {
            'true': True,
            'false': False,
            'null': None,
            'int': lambda x=0: int(x) if not isinstance(x, str) else (int(x) if x.lstrip('-').isdigit() else 0),
            'float': lambda x=0: float(x) if not isinstance(x, str) else (float(x) if x.replace('.', '', 1).lstrip('-').isdigit() else 0.0),
            'str': lambda x='': str(x) if x is not None else '',
            'bool': lambda x=False: bool(x),
            'len': lambda x=0: len(x),
            'ord': lambda s=0: ord(s[0]) if isinstance(s, str) and s else 0,
            'chr': lambda n=0: chr(int(n)),
            'type': lambda x=None: type(x).__name__,
        }
        self.import_handler = importer.ImportHandler(self)
        self.eval_handler = EvalHandler(self)
        self.modules = {}
        self.current_function = None
        self.return_value = None
        self.functions = {}
        self.loop_depth = 0
        # Global env reference — `global [x = 5]` sets here, bukan di
        # local function scope. `x = 5` sets di current scope (local).
        self.global_env = self.env
        
    def run(self, code, is_function=False):
        """Execute JPX code"""
        if not is_function:
            self.return_value = None
            
        # Remove BOM if present
        if code.startswith('\ufeff'):
            code = code[1:]
        
        # Remove comments (hanya # — `//` sekarang operator integer division,
        # bukan komentar. Sebelumnya `//` dianggap komentar yang menyebabkan
        # `print 17 // 5` kehilangan `// 5` dan jadi `print 17`.)
        lines = []
        for line in code.split('\n'):
            clean_line = []
            in_string = False
            quote_char = None
            i = 0
            while i < len(line):
                ch = line[i]

                # Handle string literals
                if ch in ('"', "'") and (i == 0 or line[i-1] != '\\'):
                    if not in_string:
                        in_string = True
                        quote_char = ch
                        clean_line.append(ch)
                    elif in_string and ch == quote_char:
                        in_string = False
                        quote_char = None
                        clean_line.append(ch)
                    else:
                        clean_line.append(ch)
                # Handle comments — hanya `#`
                elif ch == '#' and not in_string:
                    break
                else:
                    clean_line.append(ch)
                i += 1

            line = ''.join(clean_line).rstrip()
            if line:
                lines.append(line)
        
        clean_code = '\n'.join(lines)
        statements = self.split_statements(clean_code)
        
        # Execute statements
        i = 0
        while i < len(statements):
            stmt = statements[i].strip()
            if not stmt:
                i += 1
                continue
            
            try:
                # Try-catch statement
                if stmt.startswith('try ') or stmt.startswith('try{'):
                    self.handle_try_catch(stmt)

                # Switch statement
                elif stmt.startswith('switch '):
                    self.handle_switch(stmt)

                # Class definition
                elif stmt.startswith('class '):
                    self.handle_class_def(stmt)

                # Function definition
                elif stmt.startswith('function '):
                    self.handle_function_def(stmt)

                # Return statement: 'return expr;' atau 'return;' (bare return)
                elif stmt == 'return' or stmt.startswith('return ') or stmt.startswith('return;'):
                    val = self.handle_return(stmt)
                    raise exceptions.JPXReturnException(val)

                # Import statement
                elif stmt.startswith('[') and stmt.endswith(']'):
                    self.import_handler.handle(stmt)
                
                # Global variable assignment
                elif stmt.startswith('global ['):
                    self.handle_global(stmt)
                
                # If statement
                elif stmt.startswith('if '):
                    self.handle_if(stmt)
                
                # While loop
                elif stmt.startswith('while '):
                    self.handle_while(stmt)
                
                # For loop
                elif stmt.startswith('for '):
                    self.handle_for(stmt)
                
                # Break statement
                elif stmt == 'break':
                    if self.loop_depth > 0:
                        raise exceptions.JPXBreakException()
                    else:
                        raise exceptions.JPXSyntaxError("break outside loop")
                
                # Continue statement
                elif stmt == 'continue':
                    if self.loop_depth > 0:
                        raise exceptions.JPXContinueException()
                    else:
                        raise exceptions.JPXSyntaxError("continue outside loop")
                
                # End scanner (ignored)
                elif re.match(r'^end\s+scanner\s*;?$', stmt):
                    pass
                
                # Regular expression
                else:
                    self.eval_handler.eval_expression(stmt)
                    
            except exceptions.JPXBreakException:
                if self.loop_depth > 0:
                    raise
                else:
                    print("Warning: break outside loop")
            except exceptions.JPXContinueException:
                if self.loop_depth > 0:
                    raise
                else:
                    print("Warning: continue outside loop")
            except exceptions.JPXReturnException as e:
                raise e
            except exceptions.JPXExceptionWrapper as e:
                raise e
            except KeyboardInterrupt:
                print("\nExecution interrupted by user")
                return
            except Exception as e:
                # Propagate exception for try-catch to handle
                raise e
            
            i += 1
        
        return self.return_value

    def split_statements(self, code):
        """Split code into statements based on semicolons"""
        statements = []
        current = []
        depth_paren = 0      # ()
        depth_bracket = 0    # []
        depth_brace = 0      # {}
        in_string = False
        quote_char = None
        escape = False

        i = 0
        while i < len(code):
            ch = code[i]

            if in_string:
                current.append(ch)
                if ch == quote_char and not escape:
                    in_string = False
                    quote_char = None
                elif ch == '\\' and not escape:
                    escape = True
                else:
                    escape = False
                i += 1
                continue

            if ch in ('"', "'"):
                in_string = True
                quote_char = ch
                current.append(ch)
                i += 1
                continue

            if ch == '(':
                depth_paren += 1
                current.append(ch)
                i += 1
                continue

            if ch == ')':
                depth_paren -= 1
                current.append(ch)
                i += 1
                continue

            if ch == '[':
                depth_bracket += 1
                current.append(ch)
                i += 1
                continue

            if ch == ']':
                depth_bracket -= 1
                current.append(ch)
                i += 1
                continue

            if ch == '{':
                depth_brace += 1
                current.append(ch)
                i += 1
                continue

            if ch == '}':
                depth_brace -= 1
                current.append(ch)

                # Hanya finalize statement jika kita benar-benar di top-level
                # (semua depth = 0). Sebelumnya depth_paren tidak di-track,
                # sehingga `print json.encode({...})` salah dipecah saat `}`
                # ditutup — `)` sisanya jadi statement terpisah.
                if depth_brace == 0 and depth_bracket == 0 and depth_paren == 0:
                    next_chars = code[i+1:i+15].strip()
                    if (next_chars.startswith('catch')
                            or next_chars.startswith('else')
                            or next_chars.startswith('elif')):
                        i += 1
                        continue
                    else:
                        stmt = ''.join(current).strip()
                        if stmt:
                            statements.append(stmt)
                        current = []
                i += 1
                continue

            if ch == ';' and depth_paren == 0 and depth_bracket == 0 and depth_brace == 0 and not in_string:
                stmt = ''.join(current).strip()
                if stmt:
                    statements.append(stmt)
                current = []
                i += 1
                continue

            current.append(ch)
            i += 1

        # Last statement
        if current:
            stmt = ''.join(current).strip()
            if stmt:
                statements.append(stmt)

        return statements

    def handle_switch(self, stmt):
        """Handle switch statement.

        Syntax (Go-style, no fall-through):
          switch expr {
              case val1 { body1 }
              case val2 { body2 }
              default { bodyDefault }
          }

        Switch mengevaluasi expr, lalu mencari case yang value-nya == expr.
        Hanya block case yang match yang dijalankan (no fall-through).
        Jika tidak ada yang match, jalankan default (jika ada).
        """
        if not stmt.startswith('switch '):
            raise exceptions.JPXSyntaxError("Not a switch statement")

        # Cari `{` pembuka (track string)
        brace_pos = self._find_brace_pos(stmt, 7)
        if brace_pos == -1:
            raise exceptions.JPXSyntaxError("Missing '{' in switch statement")

        # Evaluasi switch expression
        switch_expr = stmt[7:brace_pos].strip()
        switch_val = self.eval_handler.eval_expression(switch_expr)

        # Extract body
        body = stmt[brace_pos:]
        block, rest = self.extract_block(body)
        rest = rest.strip()
        if rest:
            raise exceptions.JPXSyntaxError(f"Unexpected content after switch block: {rest!r}")

        # Parse cases dari block
        # Cari semua `case VALUE { ... }` dan `default { ... }`
        default_block = None
        matched_block = None
        pos = 0
        while pos < len(block):
            # Skip whitespace
            while pos < len(block) and body and body[pos:pos+1] in ' \t\n\r':
                pos += 1
            if pos >= len(block):
                break

            # Cek `default`
            if body is None:
                break
            if block[pos:pos+7] == 'default':
                pos += 7
                # Skip whitespace
                while pos < len(block) and block[pos] in ' \t\n\r':
                    pos += 1
                if pos >= len(block) or block[pos] != '{':
                    raise exceptions.JPXSyntaxError("Expected '{' after default")
                # Extract block
                depth = 1
                start = pos + 1
                pos += 1
                while pos < len(block) and depth > 0:
                    ch = block[pos]
                    # Track string
                    if ch in '"\'':
                        quote = ch
                        pos += 1
                        while pos < len(block) and block[pos] != quote:
                            if block[pos] == '\\':
                                pos += 1
                            pos += 1
                        pos += 1
                        continue
                    if ch == '{':
                        depth += 1
                    elif ch == '}':
                        depth -= 1
                        if depth == 0:
                            break
                    pos += 1
                default_block = block[start:pos].strip()
                pos += 1
                continue

            # Cek `case`
            if block[pos:pos+4] == 'case':
                pos += 4
                # Skip whitespace
                while pos < len(block) and block[pos] in ' \t\n\r':
                    pos += 1
                # Baca case value sampai `{`
                case_val_start = pos
                # Track string dan depth saat cari `{`
                in_str = False
                quote_ch = None
                while pos < len(block):
                    ch = block[pos]
                    if in_str:
                        if ch == '\\' and pos + 1 < len(block):
                            pos += 2
                            continue
                        if ch == quote_ch:
                            in_str = False
                        pos += 1
                        continue
                    if ch in '"\'':
                        in_str = True
                        quote_ch = ch
                    elif ch == '{':
                        break
                    pos += 1
                case_val_str = block[case_val_start:pos].strip()
                if pos >= len(block) or block[pos] != '{':
                    raise exceptions.JPXSyntaxError("Expected '{' after case value")

                # Extract case block
                depth = 1
                start = pos + 1
                pos += 1
                while pos < len(block) and depth > 0:
                    ch = block[pos]
                    if in_str:
                        if ch == '\\' and pos + 1 < len(block):
                            pos += 2
                            continue
                        if ch == quote_ch:
                            in_str = False
                        pos += 1
                        continue
                    if ch in '"\'':
                        in_str = True
                        quote_ch = ch
                    elif ch == '{':
                        depth += 1
                    elif ch == '}':
                        depth -= 1
                        if depth == 0:
                            break
                    pos += 1
                case_block = block[start:pos].strip()
                pos += 1

                # Evaluasi case value dan bandingkan
                if matched_block is None:
                    try:
                        case_val = self.eval_handler.eval_expression(case_val_str)
                        if case_val == switch_val:
                            matched_block = case_block
                    except Exception:
                        pass  # Skip case jika value gagal di-eval
                continue

            # Unknown token — skip
            pos += 1

        # Execute matched block atau default
        if matched_block is not None:
            self.run(matched_block)
        elif default_block is not None:
            self.run(default_block)

    def handle_try_catch(self, stmt):
        """Handle try-catch statement"""
        # Find try position
        try_pos = stmt.find('try')
        if try_pos == -1:
            raise exceptions.JPXSyntaxError("Invalid try statement")
        
        # Find opening brace
        try_brace = stmt.find('{', try_pos)
        if try_brace == -1:
            raise exceptions.JPXSyntaxError("Missing '{' in try block")
        
        # Extract try block
        depth = 1
        pos = try_brace + 1
        try_block = []
        
        while pos < len(stmt) and depth > 0:
            if stmt[pos] == '{':
                depth += 1
            elif stmt[pos] == '}':
                depth -= 1
                if depth == 0:
                    try_block = stmt[try_brace+1:pos].strip()
                    pos += 1
                    break
            pos += 1
        
        if not try_block:
            raise exceptions.JPXSyntaxError("Empty try block")
        
        # Find catch block
        rest = stmt[pos:].strip()
        if not rest.startswith('catch'):
            raise exceptions.JPXSyntaxError("Missing 'catch' after try block")
        
        # Get catch parameter
        param_start = rest.find('(')
        param_end = rest.find(')')
        if param_start == -1 or param_end == -1:
            raise exceptions.JPXSyntaxError("Invalid catch parameter")
        
        param_name = rest[param_start+1:param_end].strip()
        if not param_name:
            param_name = "e"
        
        # Extract catch block
        catch_brace = rest.find('{', param_end)
        if catch_brace == -1:
            raise exceptions.JPXSyntaxError("Missing '{' in catch block")
        
        depth = 1
        pos = catch_brace + 1
        catch_block = []
        
        while pos < len(rest) and depth > 0:
            if rest[pos] == '{':
                depth += 1
            elif rest[pos] == '}':
                depth -= 1
                if depth == 0:
                    catch_block = rest[catch_brace+1:pos].strip()
                    break
            pos += 1
        
        if not catch_block:
            raise exceptions.JPXSyntaxError("Empty catch block")
        
        # Execute with try-catch
        try:
            self.run(try_block)
        except exceptions.JPXExceptionWrapper as e:
            old_env = self.env.copy()
            self.env[param_name] = e
            try:
                self.run(catch_block)
            finally:
                self.env = old_env
        except Exception as e:
            wrapped = exceptions.JPXExceptionWrapper(e)
            old_env = self.env.copy()
            self.env[param_name] = wrapped
            try:
                self.run(catch_block)
            finally:
                self.env = old_env

    def handle_function_def(self, stmt):
        """Handle function definition"""
        # Named function: function name(params) { body }
        match = re.match(
            r'function\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(\s*(.*?)\s*\)\s*\{',
            stmt, 
            re.DOTALL
        )
        
        if match:
            name = match.group(1)
            params_str = match.group(2).strip()
            
            params = []
            if params_str:
                params = [p.strip() for p in params_str.split(',') if p.strip()]
            
            # Find body
            brace_count = 1
            body_start = stmt.find('{') + 1
            pos = body_start
            while pos < len(stmt) and brace_count > 0:
                if stmt[pos] == '{':
                    brace_count += 1
                elif stmt[pos] == '}':
                    brace_count -= 1
                pos += 1
            
            body = stmt[body_start:pos-1].strip()
            
            # Create and store function
            func = JPXFunction(name, params, body, self)
            self.env[name] = func
            self.functions[name] = func
            return func
        
        # Anonymous function: var = function(params) { body }
        if '=' in stmt and 'function' in stmt:
            eq_pos = stmt.find('=')
            var_name = stmt[:eq_pos].strip()
            rest = stmt[eq_pos+1:].strip()
            
            match = re.match(
                r'function\s*\(\s*(.*?)\s*\)\s*\{',
                rest,
                re.DOTALL
            )
            
            if match:
                params_str = match.group(1).strip()
                params = [p.strip() for p in params_str.split(',') if p.strip()]
                
                brace_count = 1
                body_start = rest.find('{') + 1
                pos = body_start
                while pos < len(rest) and brace_count > 0:
                    if rest[pos] == '{':
                        brace_count += 1
                    elif rest[pos] == '}':
                        brace_count -= 1
                    pos += 1
                
                body = rest[body_start:pos-1].strip()
                
                func = JPXFunction(var_name, params, body, self, is_anonymous=True)
                self.env[var_name] = func
                self.functions[var_name] = func
                return func
        
        raise exceptions.JPXSyntaxError("Invalid function definition")

    def handle_return(self, stmt):
        """Handle return statement"""
        expr = stmt[7:].strip()
        if expr:
            return self.eval_handler.eval_expression(expr)
        return None

    def handle_global(self, stmt):
        """Handle global variable assignment: global [var = value]"""
        m = re.match(r'global\s*\[(.*)\]', stmt, re.DOTALL)
        if not m:
            raise exceptions.JPXSyntaxError("Invalid global statement")
        
        inner = m.group(1).strip()
        if inner.endswith(';'):
            inner = inner[:-1].strip()
        
        parts = inner.split('=', 1)
        if len(parts) != 2:
            raise exceptions.JPXSyntaxError("Invalid assignment in global")
        
        var_name = parts[0].strip()
        value = self.eval_handler.eval_expression(parts[1].strip())

        # Catatan: sebelumnya ada blok "Type conversion" yang mengubah
        # string digit menjadi int/float otomatis (mis. "123" -> 123).
        # Ini BURUK karena string yang sengaja berisi angka (mis. "123abc"
        # sebagai data tekstual) rusak. Untuk konversi, user harus pakai
        # int(...) atau float(...) secara eksplisit.

        # Evaluasi value dengan MERGED env: global values (current) + local
        # values (parameters, locals). Global values diutamakan — local vars
        # hanya ditambahkan jika TIDAK ada di global. Ini memastikan:
        # - `counter` (global) dibaca dari global_env (current value)
        # - `arr` (parameter, local-only) tetap terlihat
        old_env = self.env
        merged = dict(self.global_env)  # global first (current values)
        for k, v in self.env.items():
            if k not in merged:  # only add local vars not in global
                merged[k] = v
        self.env = merged
        value = self.eval_handler.eval_expression(parts[1].strip())
        self.env = old_env

        # Write ke global env (persistent) dan local env (untuk reads berikutnya)
        self.global_env[var_name] = value
        old_env[var_name] = value

    def get_value(self, ident):
        """Get value from identifier"""
        parts = ident.split('.')

        # Check local env first, then global env, then functions, then builtins.
        if parts[0] in self.env:
            obj = self.env[parts[0]]
        elif parts[0] in self.global_env:
            obj = self.global_env[parts[0]]
        elif parts[0] in self.functions:
            obj = self.functions[parts[0]]
        elif parts[0] in self.builtins:
            obj = self.builtins[parts[0]]
        else:
            raise exceptions.JPXNameError(f"Undefined variable: {parts[0]}")
        
        # Navigate through dots
        for part in parts[1:]:
            if '[' in part and ']' in part:
                bracket_pos = part.find('[')
                attr = part[:bracket_pos]
                index_str = part[bracket_pos+1:-1].strip()
                
                if attr:
                    obj = getattr(obj, attr)
                
                # Evaluate index
                if index_str.startswith('"') and index_str.endswith('"'):
                    index = index_str[1:-1]
                elif index_str.isdigit():
                    index = int(index_str)
                else:
                    index = self.eval_handler.eval_expression(index_str)
                    if isinstance(index, str) and index.isdigit():
                        index = int(index)
                
                obj = obj[index]
            else:
                if isinstance(obj, dict):
                    obj = obj.get(part)
                else:
                    obj = getattr(obj, part)
        return obj

    def set_builtin(self, name, obj):
        """Set builtin function/variable"""
        self.builtins[name] = obj

    def _find_brace_pos(self, stmt, start=0):
        """Cari posisi `{` pembuka block, track string literals agar `{`
        di dalam string tidak salah dianggap brace. Return -1 kalau tidak
        ketemu."""
        in_str = False
        quote_ch = None
        i = start
        while i < len(stmt):
            ch = stmt[i]
            if in_str:
                if ch == '\\' and i + 1 < len(stmt):
                    i += 2
                    continue
                if ch == quote_ch:
                    in_str = False
                i += 1
                continue
            if ch in '"\'':
                in_str = True
                quote_ch = ch
            elif ch == '{':
                return i
            i += 1
        return -1

    def handle_if(self, stmt):
        """Handle if-elif-else statement.

        Syntax yang didukung:
          if cond { ... }
          if cond { ... } else { ... }
          if cond { ... } elif cond2 { ... } else { ... }

        `elif` di-handle dengan recursive call ke handle_if untuk blok
        berikutnya, sehingga chain panjang tetap efisien.
        """
        if not stmt.startswith('if '):
            raise exceptions.JPXSyntaxError("Not an if statement")

        # Cari `{` pembuka block, track string literals.
        brace_pos = self._find_brace_pos(stmt, 3)
        if brace_pos == -1:
            raise exceptions.JPXSyntaxError("Missing '{' in if statement")

        condition = stmt[3:brace_pos].strip()
        block_if, rest = self.extract_block(stmt[brace_pos:])

        # Cek else / elif setelah block_if
        block_else = None
        rest = rest.strip()
        if rest.startswith('elif'):
            # elif: re-parse sebagai if statement baru
            # dengan prefix 'if ' agar handle_if accept.
            # rest = "elif cond { ... } else { ... }"
            # ubah jadi "if cond { ... } else { ... }"
            elif_body = 'if ' + rest[5:].lstrip()
            block_else = elif_body  # recursive call akan handle
        elif rest.startswith('else'):
            # else { ... }
            else_rest = rest[4:].strip()
            if else_rest.startswith('if'):
                # `else if` (alternative syntax untuk elif)
                block_else = else_rest
            else:
                block_else, _ = self.extract_block(else_rest)

        # Evaluate condition
        cond_val = self.eval_handler.eval_expression(condition)

        if self.is_truthy(cond_val):
            self.run(block_if)
        elif block_else is not None:
            # Jika block_else berawalan 'if ', recursive handle_if
            if isinstance(block_else, str) and block_else.startswith('if '):
                self.handle_if(block_else)
            else:
                self.run(block_else)

    def handle_while(self, stmt):
        """Handle while loop"""
        if not stmt.startswith('while '):
            raise exceptions.JPXSyntaxError("Not a while statement")

        brace_pos = self._find_brace_pos(stmt, 6)
        if brace_pos == -1:
            raise exceptions.JPXSyntaxError("Missing '{' in while statement")

        condition = stmt[6:brace_pos].strip()
        block, _ = self.extract_block(stmt[brace_pos:])
        
        self.loop_depth += 1
        try:
            while True:
                try:
                    cond_val = self.eval_handler.eval_expression(condition)
                    if not cond_val:
                        break
                    self.run(block)
                except exceptions.JPXBreakException:
                    break
                except exceptions.JPXContinueException:
                    continue
        finally:
            self.loop_depth -= 1

    def handle_for(self, stmt):
        """Handle for loop"""
        # Format: for var = start to end
        m = re.match(r'for\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.+?)\s+to\s+(.+?)\s*{', stmt, re.DOTALL)
        if m:
            var_name = m.group(1)
            start_expr = m.group(2).strip()
            end_expr = m.group(3).strip()

            brace_pos = self._find_brace_pos(stmt)
            block, _ = self.extract_block(stmt[brace_pos:])
            
            start_val = self.eval_handler.eval_expression(start_expr)
            end_val = self.eval_handler.eval_expression(end_expr)

            # Bounds harus int/float. String digit gak otomatis dikonversi
            # (pakai int(...) / float(...) eksplisit jika perlu).
            if not isinstance(start_val, (int, float)) or isinstance(start_val, bool):
                raise exceptions.JPXTypeError("For loop start must be a number")
            if not isinstance(end_val, (int, float)) or isinstance(end_val, bool):
                raise exceptions.JPXTypeError("For loop end must be a number")
            
            start_num = int(start_val)
            end_num = int(end_val)
            
            self.loop_depth += 1
            try:
                i = start_num
                while i <= end_num:
                    self.env[var_name] = i
                    try:
                        self.run(block)
                    except exceptions.JPXBreakException:
                        break
                    except exceptions.JPXContinueException:
                        i += 1
                        continue
                    i += 1
            finally:
                self.loop_depth -= 1
            
            return
        
        # Format: for item in list
        m = re.match(r'for\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+in\s+(.+?)\s*{', stmt, re.DOTALL)
        if m:
            var_name = m.group(1)
            list_expr = m.group(2).strip()

            brace_pos = self._find_brace_pos(stmt)
            block, _ = self.extract_block(stmt[brace_pos:])
            
            list_val = self.eval_handler.eval_expression(list_expr)
            
            if not isinstance(list_val, (list, tuple)):
                raise exceptions.JPXTypeError("For loop 'in' requires a list")
            
            self.loop_depth += 1
            try:
                for item in list_val:
                    self.env[var_name] = item
                    try:
                        self.run(block)
                    except exceptions.JPXBreakException:
                        break
                    except exceptions.JPXContinueException:
                        continue
            finally:
                self.loop_depth -= 1
            
            return
        
        raise exceptions.JPXSyntaxError("Invalid for loop syntax")

    def extract_block(self, s):
        """Extract block of code inside {...}.
        Track string literals agar `{` atau `}` di dalam string tidak
        salah dihitung sebagai brace."""
        if not s.startswith('{'):
            raise exceptions.JPXSyntaxError("Expected '{'")

        depth = 0
        in_str = False
        quote_ch = None
        i = 0
        while i < len(s):
            ch = s[i]
            if in_str:
                if ch == '\\' and i + 1 < len(s):
                    i += 2
                    continue
                if ch == quote_ch:
                    in_str = False
                i += 1
                continue
            if ch in '"\'':
                in_str = True
                quote_ch = ch
            elif ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    return s[1:i], s[i+1:].lstrip()
            i += 1

        raise exceptions.JPXSyntaxError("Unclosed block")

    def is_truthy(self, val):
        """Check if value is truthy for conditions"""
        if val is None:
            return False
        if isinstance(val, bool):
            return val
        if isinstance(val, (int, float)):
            return val != 0
        if isinstance(val, str):
            # Hanya "true"/"false" (case-insensitive) dan empty check.
            # Sebelumnya "0"/"1" dianggap numerik truthy, tapi ini
            # kontras dengan string biasa — string "0" mestinya truthy
            # (non-empty string). Konsisten dengan Python/JS.
            if val.lower() == 'true':
                return True
            if val.lower() == 'false':
                return False
            return val != ""
        if isinstance(val, (list, dict)):
            return len(val) > 0
        return True

    # ============================================================
    # CLASS SUPPORT
    # ============================================================

    def handle_class_def(self, stmt):
        """Handle class definition.

        Syntax (methods TANPA keyword `function` — mirip Python/JS):
          class Name {
              __init__(params) { ... }    # constructor (opsional)
              method1(params) { ... }
              method2(params) { ... }
          }

        Class disimpan sebagai dict dengan key:
          '__jpx_class__'  : True
          'name'           : class name
          'init'           : JPXFunction untuk __init__ (atau None)
          'methods'        : dict nama_method -> JPXFunction

        Instance dibuat dengan `ClassName(args)` — syntax yang sama dengan
        function call. Instance adalah dict dengan key:
          '__class__'  : reference ke class
          'fields'     : dict field name -> value
        """
        import re as _re
        m = _re.match(r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\{', stmt)
        if not m:
            raise exceptions.JPXSyntaxError("Invalid class definition")

        class_name = m.group(1)
        body_start = stmt.find('{') + 1

        # Extract body dengan brace matching.
        # Track string literals agar `}` di dalam string tidak dianggap
        # sebagai closing brace dari class body.
        depth = 1
        pos = body_start
        in_str = False
        quote_ch = None
        while pos < len(stmt) and depth > 0:
            ch = stmt[pos]
            if in_str:
                if ch == '\\' and pos + 1 < len(stmt):
                    pos += 2
                    continue
                if ch == quote_ch:
                    in_str = False
                pos += 1
                continue
            if ch in '"\'':
                in_str = True
                quote_ch = ch
            elif ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    break
            pos += 1
        body = stmt[body_start:pos].strip()

        # Parse body — methods tanpa keyword `function`, langsung
        # `methodName(params) { body }`
        cls = {
            '__jpx_class__': True,
            'name': class_name,
            'init': None,
            'methods': {}
        }

        # Scan manual untuk handle nested braces.
        # PENTING: track string literals agar `(`, `)`, `{`, `}` di dalam
        # string tidak dihitung sebagai bracket pembuka/penutup.
        i = 0
        while i < len(body):
            # Skip whitespace dan komentar
            while i < len(body) and body[i] in ' \t\n':
                i += 1
            if i >= len(body):
                break
            # Baca nama method (IDENT)
            name_match = _re.match(r'([a-zA-Z_][a-zA-Z0-9_]*)', body[i:])
            if not name_match:
                # Skip char (mungkin komentar)
                i += 1
                continue
            method_name = name_match.group(1)
            i += name_match.end()

            # Skip whitespace
            while i < len(body) and body[i] in ' \t\n':
                i += 1

            # Harus ada `(`
            if i >= len(body) or body[i] != '(':
                # Bukan method, skip (mungkin class field — belum didukung)
                continue

            # Match parens untuk ambil params (track string!)
            depth_p = 1
            param_start = i + 1
            i += 1
            in_str = False
            quote_ch = None
            while i < len(body) and depth_p > 0:
                ch = body[i]
                if in_str:
                    if ch == '\\' and i + 1 < len(body):
                        i += 2
                        continue
                    if ch == quote_ch:
                        in_str = False
                    i += 1
                    continue
                if ch in '"\'':
                    in_str = True
                    quote_ch = ch
                elif ch == '(':
                    depth_p += 1
                elif ch == ')':
                    depth_p -= 1
                    if depth_p == 0:
                        break
                i += 1
            params_str = body[param_start:i].strip()
            params = [p.strip() for p in params_str.split(',') if p.strip()]
            i += 1  # skip )

            # Skip whitespace sebelum {
            while i < len(body) and body[i] in ' \t\n':
                i += 1
            if i >= len(body) or body[i] != '{':
                continue
            # Match braces untuk ambil method body (track string!)
            depth_b = 1
            body_start_m = i + 1
            i += 1
            in_str = False
            quote_ch = None
            while i < len(body) and depth_b > 0:
                ch = body[i]
                if in_str:
                    if ch == '\\' and i + 1 < len(body):
                        i += 2
                        continue
                    if ch == quote_ch:
                        in_str = False
                    i += 1
                    continue
                if ch in '"\'':
                    in_str = True
                    quote_ch = ch
                elif ch == '{':
                    depth_b += 1
                elif ch == '}':
                    depth_b -= 1
                    if depth_b == 0:
                        break
                i += 1
            method_body = body[body_start_m:i].strip()
            i += 1  # skip }

            # Buat JPXFunction untuk method ini
            from .function import JPXFunction
            method_func = JPXFunction(method_name, params, method_body, self)
            if method_name == '__init__':
                cls['init'] = method_func
            else:
                cls['methods'][method_name] = method_func

        # Late binding fix-up: setelah semua method di-defined, update
        # closure_env setiap method agar include semua sibling methods.
        # Sebelumnya, method A tidak bisa call method B karena B belum ada
        # di closure snapshot A saat di-defined.
        all_methods = {}
        if cls['init'] is not None:
            all_methods['__init__'] = cls['init']
        for mname, mfn in cls['methods'].items():
            all_methods[mname] = mfn
        for mname, mfn in all_methods.items():
            for k, v in all_methods.items():
                if k not in mfn.closure_env:
                    mfn.closure_env[k] = v
            # Juga inject class itu sendiri agar bisa instantiate
            mfn.closure_env[class_name] = cls

        # Simpan class ke env (bisa di-instantiate dengan ClassName(args))
        self.env[class_name] = cls
        self.functions[class_name] = cls  # agar get_value menemukan
        return cls