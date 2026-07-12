"""
JpXui - GUI Library untuk JPX (Windows only)
Menggunakan ctypes WinAPI dengan pendekatan deklaratif.
Event handler ditulis sebagai string kode JPX.
"""

import ctypes
from ctypes import wintypes
import threading

# ========== Definisi tipe yang mungkin hilang di Python 3.14 ==========
if not hasattr(wintypes, 'LRESULT'):
    wintypes.LRESULT = ctypes.c_long
if not hasattr(wintypes, 'LPARAM'):
    wintypes.LPARAM = ctypes.c_long
if not hasattr(wintypes, 'WPARAM'):
    wintypes.WPARAM = ctypes.c_uint
if not hasattr(wintypes, 'LONG_PTR'):
    wintypes.LONG_PTR = ctypes.c_long
if not hasattr(wintypes, 'HBRUSH'):
    wintypes.HBRUSH = ctypes.c_void_p
if not hasattr(wintypes, 'HCURSOR'):
    wintypes.HCURSOR = ctypes.c_void_p
if not hasattr(wintypes, 'HICON'):
    wintypes.HICON = ctypes.c_void_p
if not hasattr(wintypes, 'HMENU'):
    wintypes.HMENU = ctypes.c_void_p
if not hasattr(wintypes, 'HINSTANCE'):
    wintypes.HINSTANCE = ctypes.c_void_p
if not hasattr(wintypes, 'HWND'):
    wintypes.HWND = ctypes.c_void_p
if not hasattr(wintypes, 'HDC'):
    wintypes.HDC = ctypes.c_void_p
if not hasattr(wintypes, 'UINT'):
    wintypes.UINT = ctypes.c_uint
if not hasattr(wintypes, 'DWORD'):
    wintypes.DWORD = ctypes.c_ulong
if not hasattr(wintypes, 'BOOL'):
    wintypes.BOOL = ctypes.c_long
if not hasattr(wintypes, 'LPWSTR'):
    wintypes.LPWSTR = ctypes.c_wchar_p
if not hasattr(wintypes, 'LPCWSTR'):
    wintypes.LPCWSTR = ctypes.c_wchar_p
if not hasattr(wintypes, 'INT'):
    wintypes.INT = ctypes.c_int
if not hasattr(wintypes, 'COLORREF'):
    wintypes.COLORREF = ctypes.c_ulong

# ========== Konstanta Windows ==========
WS_OVERLAPPEDWINDOW = 0x00CF0000
WS_VISIBLE = 0x10000000
WS_CHILD = 0x40000000
BS_PUSHBUTTON = 0x00000000
BS_AUTOCHECKBOX = 0x00000003
BS_AUTORADIOBUTTON = 0x00000009
BS_GROUPBOX = 0x00000007
ES_LEFT = 0x00000000
ES_AUTOHSCROLL = 0x00000080
WS_BORDER = 0x00800000
WS_TABSTOP = 0x00010000
WS_GROUP = 0x00020000
SS_LEFT = 0x00000000
WM_COMMAND = 0x0111
WM_CLOSE = 0x0010
WM_DESTROY = 0x0002
COLOR_WINDOW = 5
SWP_NOMOVE = 0x0002
SWP_NOZORDER = 0x0004

# ========== Struktur ==========
class WNDCLASSEXW(ctypes.Structure):
    _fields_ = [
        ('cbSize', wintypes.UINT),
        ('style', wintypes.UINT),
        ('lpfnWndProc', ctypes.c_void_p),
        ('cbClsExtra', ctypes.c_int),
        ('cbWndExtra', ctypes.c_int),
        ('hInstance', wintypes.HINSTANCE),
        ('hIcon', wintypes.HICON),
        ('hCursor', wintypes.HCURSOR),
        ('hbrBackground', wintypes.HBRUSH),
        ('lpszMenuName', wintypes.LPCWSTR),
        ('lpszClassName', wintypes.LPCWSTR),
        ('hIconSm', wintypes.HICON)
    ]

class MSG(ctypes.Structure):
    _fields_ = [
        ('hwnd', wintypes.HWND),
        ('message', wintypes.UINT),
        ('wParam', wintypes.WPARAM),
        ('lParam', wintypes.LPARAM),
        ('time', wintypes.DWORD),
        ('pt', wintypes.POINT)
    ]

# ========== Load library ==========
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# ========== Fungsi-fungsi Windows ==========
user32.CreateWindowExW.argtypes = [
    wintypes.DWORD, wintypes.LPCWSTR, wintypes.LPCWSTR,
    wintypes.DWORD, ctypes.c_int, ctypes.c_int,
    ctypes.c_int, ctypes.c_int, wintypes.HWND,
    wintypes.HMENU, wintypes.HINSTANCE, ctypes.c_void_p
]
user32.CreateWindowExW.restype = wintypes.HWND

user32.DefWindowProcW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
user32.DefWindowProcW.restype = wintypes.LRESULT

user32.RegisterClassW.argtypes = [ctypes.POINTER(WNDCLASSEXW)]
user32.RegisterClassW.restype = wintypes.ATOM

user32.GetMessageW.argtypes = [ctypes.POINTER(MSG), wintypes.HWND, wintypes.UINT, wintypes.UINT]
user32.GetMessageW.restype = wintypes.BOOL

user32.TranslateMessage.argtypes = [ctypes.POINTER(MSG)]
user32.DispatchMessageW.argtypes = [ctypes.POINTER(MSG)]
user32.PostQuitMessage.argtypes = [ctypes.c_int]

user32.SetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPCWSTR]
user32.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
user32.GetWindowTextLengthW.argtypes = [wintypes.HWND]
user32.ShowWindow.argtypes = [wintypes.HWND, ctypes.c_int]
user32.UpdateWindow.argtypes = [wintypes.HWND]
user32.SendMessageW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
user32.DestroyWindow.argtypes = [wintypes.HWND]
user32.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint]

# ========== Global interpreter ==========
_interpreter = None

def set_interpreter(interp):
    global _interpreter
    _interpreter = interp

# ========== Kelas JpXui ==========
class JpXui:
    def __init__(self):
        self.hinstance = kernel32.GetModuleHandleW(None)
        self.windows = []
        self.callbacks = {}          # id kontrol -> string kode JPX
        self.controls = {}           # id kontrol -> (window, hwnd) untuk akses
        self.next_id = 1000
        self.running = False

        # Window procedure
        WNDPROC = ctypes.WINFUNCTYPE(wintypes.LRESULT, wintypes.HWND, wintypes.UINT,
                                      wintypes.WPARAM, wintypes.LPARAM)
        self._wndproc = WNDPROC(self._window_proc)

        # Daftarkan kelas window
        wc = WNDCLASSEXW()
        wc.cbSize = ctypes.sizeof(WNDCLASSEXW)
        wc.style = 3  # CS_HREDRAW | CS_VREDRAW
        wc.lpfnWndProc = ctypes.cast(self._wndproc, ctypes.c_void_p).value
        wc.hInstance = self.hinstance
        wc.hbrBackground = COLOR_WINDOW + 1
        wc.lpszClassName = "JpXWindowClass"
        user32.RegisterClassW(ctypes.byref(wc))

    def _window_proc(self, hwnd, msg, wparam, lparam):
        if msg == WM_COMMAND:
            ctrl_id = wparam & 0xFFFF
            if ctrl_id in self.callbacks:
                code = self.callbacks[ctrl_id]
                if _interpreter and code:
                    _interpreter.run(code)
        elif msg == WM_CLOSE:
            user32.DestroyWindow(hwnd)
        elif msg == WM_DESTROY:
            # Hapus dari daftar window
            self.windows = [w for w in self.windows if w.hwnd != hwnd]
            if not self.windows:
                user32.PostQuitMessage(0)
        return user32.DefWindowProcW(hwnd, msg, wparam, lparam)

    def _message_loop(self):
        self.running = True
        msg = MSG()
        while self.running:
            ret = user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
            if ret <= 0:
                break
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))
        self.running = False

    def App(self, title="JPX App", width=400, height=300):
        """Buat window baru, kembalikan objek JpXWindow"""
        win = JpXWindow(self, title, width, height)
        self.windows.append(win)
        return win

    def _next_id(self):
        self.next_id += 1
        return self.next_id

# ========== Kelas Window ==========
class JpXWindow:
    def __init__(self, ui, title, width, height):
        self.ui = ui
        self.hwnd = user32.CreateWindowExW(
            0, "JpXWindowClass", title,
            WS_OVERLAPPEDWINDOW | WS_VISIBLE,
            100, 100, width, height,
            None, None, ui.hinstance, None
        )
        user32.ShowWindow(self.hwnd, 1)
        user32.UpdateWindow(self.hwnd)

        # Simpan mapping id -> hwnd kontrol untuk akses cepat
        self.controls = {}   # id_kontrol -> hwnd

    def config(self, props):
        """Mengatur properti window (title, width, height)"""
        if 'title' in props:
            user32.SetWindowTextW(self.hwnd, props['title'])
        if 'width' in props and 'height' in props:
            user32.SetWindowPos(self.hwnd, 0, 0, 0, props['width'], props['height'], SWP_NOMOVE | SWP_NOZORDER)

    def add(self, comp):
        """
        Menambahkan komponen.
        comp adalah dictionary dengan field:
          - type: "label", "button", "textbox", "checkbox", "radio", "groupbox"
          - text: string
          - x, y, width, height: integer
          - onclick (untuk button): string kode JPX
          - checked (untuk checkbox/radio): boolean
        Mengembalikan id komponen.
        """
        tipe = comp.get('type')
        x = comp.get('x', 0)
        y = comp.get('y', 0)
        w = comp.get('width', 80)
        h = comp.get('height', 30)
        text = comp.get('text', '')
        ctrl_id = self.ui._next_id()

        if tipe == 'label':
            hwnd = user32.CreateWindowExW(
                0, "STATIC", text,
                WS_VISIBLE | WS_CHILD | SS_LEFT,
                x, y, w, h, self.hwnd, None, self.ui.hinstance, None
            )
            self.controls[ctrl_id] = hwnd
        elif tipe == 'button':
            style = WS_VISIBLE | WS_CHILD | BS_PUSHBUTTON | WS_TABSTOP
            hwnd = user32.CreateWindowExW(
                0, "BUTTON", text, style,
                x, y, w, h, self.hwnd, ctrl_id, self.ui.hinstance, None
            )
            if 'onclick' in comp:
                self.ui.callbacks[ctrl_id] = comp['onclick']
            self.controls[ctrl_id] = hwnd
        elif tipe == 'textbox':
            style = WS_VISIBLE | WS_CHILD | WS_BORDER | ES_LEFT | ES_AUTOHSCROLL
            hwnd = user32.CreateWindowExW(
                0, "EDIT", text, style,
                x, y, w, h, self.hwnd, None, self.ui.hinstance, None
            )
            self.controls[ctrl_id] = hwnd
        elif tipe == 'checkbox':
            style = WS_VISIBLE | WS_CHILD | BS_AUTOCHECKBOX | WS_TABSTOP
            hwnd = user32.CreateWindowExW(
                0, "BUTTON", text, style,
                x, y, w, h, self.hwnd, ctrl_id, self.ui.hinstance, None
            )
            if 'checked' in comp:
                state = 1 if comp['checked'] else 0
                user32.SendMessageW(hwnd, 0x00F1, state, 0)
            if 'onclick' in comp:
                self.ui.callbacks[ctrl_id] = comp['onclick']
            self.controls[ctrl_id] = hwnd
        elif tipe == 'radio':
            style = WS_VISIBLE | WS_CHILD | BS_AUTORADIOBUTTON | WS_TABSTOP | WS_GROUP
            hwnd = user32.CreateWindowExW(
                0, "BUTTON", text, style,
                x, y, w, h, self.hwnd, ctrl_id, self.ui.hinstance, None
            )
            if 'checked' in comp:
                state = 1 if comp['checked'] else 0
                user32.SendMessageW(hwnd, 0x00F1, state, 0)
            if 'onclick' in comp:
                self.ui.callbacks[ctrl_id] = comp['onclick']
            self.controls[ctrl_id] = hwnd
        elif tipe == 'groupbox':
            style = WS_VISIBLE | WS_CHILD | BS_GROUPBOX
            hwnd = user32.CreateWindowExW(
                0, "BUTTON", text, style,
                x, y, w, h, self.hwnd, None, self.ui.hinstance, None
            )
            self.controls[ctrl_id] = hwnd
        else:
            return None

        return ctrl_id

    def get_text(self, ctrl_id):
        if ctrl_id not in self.controls:
            return ""
        hwnd = self.controls[ctrl_id]
        length = user32.GetWindowTextLengthW(hwnd) + 1
        buf = ctypes.create_unicode_buffer(length)
        user32.GetWindowTextW(hwnd, buf, length)
        return buf.value

    def set_text(self, ctrl_id, text):
        if ctrl_id in self.controls:
            user32.SetWindowTextW(self.controls[ctrl_id], text)

    def get_checked(self, ctrl_id):
        if ctrl_id not in self.controls:
            return False
        hwnd = self.controls[ctrl_id]
        state = user32.SendMessageW(hwnd, 0x00F0, 0, 0)
        return state == 1

    def set_checked(self, ctrl_id, checked):
        if ctrl_id in self.controls:
            state = 1 if checked else 0
            user32.SendMessageW(self.controls[ctrl_id], 0x00F1, state, 0)

    def loop(self):
        self.ui._message_loop()

# ========== Ekspor ==========
exports = {
    'JpXui': JpXui()
}
