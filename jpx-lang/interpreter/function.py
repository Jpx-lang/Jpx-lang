"""
JPXFunction class - Representasi fungsi di JPX
"""

# Re-export JPXReturnException dari exceptions agar ada satu sumber kebenaran.
# Sebelumnya class ini didefinisikan duplikat di function.py dan exceptions.py,
# sehingga `isinstance(e, JPXReturnException)` gagal dan return value tidak
# pernah sampai ke caller.
from .exceptions import JPXReturnException  # noqa: F401,E402  (re-export)

class JPXFunction:
    """Representasi fungsi di JPX"""
    def __init__(self, name, params, body, interpreter, is_anonymous=False, closure_env=None):
        self.name = name
        self.params = params  # List parameter
        self.body = body      # Kode function
        self.interpreter = interpreter  # Reference ke interpreter
        self.is_anonymous = is_anonymous
        # Closure env: snapshot environment saat function DIDEFINISIKAN.
        # Sebelumnya default-nya {} — function tidak pernah menangkap variabel
        # parent scope, sehingga inner function tidak bisa lihat outer variable.
        # Sekarang: kalau closure_env None, snapshot env interpreter saat ini.
        if closure_env is None:
            self.closure_env = dict(interpreter.env)
        else:
            self.closure_env = closure_env

    def call(self, args):
        """Panggil fungsi dengan arguments"""
        # Simpan environment lama
        old_env = self.interpreter.env
        old_return = self.interpreter.return_value

        try:
            # Environment baru = closure env (variabel yang ditangkap saat
            # function didefinisikan) + parameter. Tidak pakai old_env agar
            # function call bersifat lexical-scoped, bukan dynamic.
            new_env = dict(self.closure_env)
            for i, param in enumerate(self.params):
                if i < len(args):
                    new_env[param] = args[i]
                else:
                    new_env[param] = None
            self.interpreter.env = new_env

            # Reset return value
            self.interpreter.return_value = None

            # Jalankan body function
            self.interpreter.run(self.body, is_function=True)

            # Return value (nilai dari return statement)
            return self.interpreter.return_value

        except JPXReturnException as e:
            # Return dari function
            return e.value
        finally:
            # Restore environment
            self.interpreter.env = old_env
            self.interpreter.return_value = old_return
    
    def __call__(self, *args):
        """Membuat objek function bisa dipanggil seperti fungsi biasa"""
        return self.call(list(args))
    
    def __repr__(self):
        if self.name:
            return f"<function {self.name}>"
        else:
            return "<anonymous function>"