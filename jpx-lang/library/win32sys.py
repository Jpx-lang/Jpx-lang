"""
win32.py - Windows Native API Super Lengkap untuk JPX
Mengakses hampir semua fungsi Windows API via pywin32
"""

import sys
import os
import time
import json

# Cek ketersediaan pywin32
try:
    import win32api
    import win32con
    import win32gui
    import win32gui_struct
    import win32process
    import win32file
    import win32pipe
    import win32security
    import win32event
    import win32service
    import win32serviceutil
    import win32print
    import win32clipboard
    import win32com.client
    import win32com.shell.shell as shell
    import win32com.shell.shellcon as shellcon
    import win32net
    import win32netcon
    import win32profile
    import win32crypt
    import win32cred
    import win32pdh
    import win32pdhquery
    import win32ras
    import win32ts
    import win32wts
    import win32ver
    import win32evtlog
    import win32evtlogutil
    import win32job
    import win32kernel32
    import win32timezone
    import win32transaction
    import win32wnet
    import pywintypes
    WIN32_AVAILABLE = True
except ImportError as e:
    WIN32_AVAILABLE = False
    print(f"⚠️  pywin32 error: {e}")

class Win32:
    def __init__(self):
        self.is_available = WIN32_AVAILABLE
        if not self.is_available:
            print("⚠️  pywin32 tidak terinstall. Install: pip install pywin32")
    
    # ========== SISTEM INFORMASI ==========
    def get_computer_name(self):
        """Nama komputer di jaringan"""
        if not self.is_available: return None
        return win32api.GetComputerName()
    
    def get_computer_name_ex(self):
        """Nama komputer lengkap (termasuk domain)"""
        if not self.is_available: return None
        return win32api.GetComputerNameEx(win32con.ComputerNameDnsFullyQualified)
    
    def get_user_name(self):
        """Username yang sedang login"""
        if not self.is_available: return None
        return win32api.GetUserName()
    
    def get_user_name_ex(self):
        """Username lengkap dengan domain"""
        if not self.is_available: return None
        return win32api.GetUserNameEx(win32con.NameDisplay)
    
    def get_windows_version(self):
        """Versi Windows lengkap"""
        if not self.is_available: return None
        return win32api.GetVersionEx()
    
    def get_windows_build(self):
        """Build number Windows"""
        if not self.is_available: return 0
        return win32api.GetVersionEx()[3]
    
    def get_system_info(self):
        """Informasi sistem lengkap"""
        if not self.is_available: return {}
        info = win32api.GetSystemInfo()
        return {
            'processor_arch': info[0],
            'page_size': info[1],
            'min_app_addr': info[2],
            'max_app_addr': info[3],
            'active_processor_mask': info[4],
            'num_processors': info[5],
            'processor_type': info[6],
            'allocation_granularity': info[7],
            'processor_level': info[8],
            'processor_revision': info[9]
        }
    
    def get_system_metrics(self, index):
        """Ukuran elemen sistem"""
        if not self.is_available: return 0
        metrics = {
            'screen_width': win32con.SM_CXSCREEN,
            'screen_height': win32con.SM_CYSCREEN,
            'cursor_width': win32con.SM_CXCURSOR,
            'cursor_height': win32con.SM_CYCURSOR,
            'menu_height': win32con.SM_CYMENU,
            'caption_height': win32con.SM_CYCAPTION,
            'border_width': win32con.SM_CXBORDER,
            'border_height': win32con.SM_CYBORDER,
            'scroll_width': win32con.SM_CXVSCROLL,
            'scroll_height': win32con.SM_CYHSCROLL,
            'icon_width': win32con.SM_CXICON,
            'icon_height': win32con.SM_CYICON,
            'cxmin': win32con.SM_CXMIN,
            'cymin': win32con.SM_CYMIN,
            'cxmaximized': win32con.SM_CXMAXIMIZED,
            'cymaximized': win32con.SM_CYMAXIMIZED,
            'cxfullscreen': win32con.SM_CXFULLSCREEN,
            'cyfullscreen': win32con.SM_CYFULLSCREEN,
            'mouse_present': win32con.SM_MOUSEPRESENT,
            'debug': win32con.SM_DEBUG,
            'swapbutton': win32con.SM_SWAPBUTTON,
            'cxminimized': win32con.SM_CXMINIMIZED,
            'cyminimized': win32con.SM_CYMINIMIZED,
            'cxsize': win32con.SM_CXSIZE,
            'cysize': win32con.SM_CYSIZE,
            'cxframe': win32con.SM_CXFRAME,
            'cyframe': win32con.SM_CYFRAME,
            'cxminspacing': win32con.SM_CXMINSPACING,
            'cyminspacing': win32con.SM_CYMINSPACING,
            'cxsmicon': win32con.SM_CXSMICON,
            'cysmicon': win32con.SM_CYSMICON,
            'cxsmcaption': win32con.SM_CXSMCAPTION,
            'cysmcaption': win32con.SM_CYSMCAPTION,
            'cxmenu': win32con.SM_CXMENUSIZE,
            'cymenu': win32con.SM_CYMENUSIZE,
            'cxmenuchecks': win32con.SM_CXMENUCHECK,
            'cymenuchecks': win32con.SM_CYMENUCHECK,
            'network': win32con.SM_NETWORK,
            'penwindows': win32con.SM_PENWINDOWS,
            'secure': win32con.SM_SECURE,
            'cxedge': win32con.SM_CXEDGE,
            'cyedge': win32con.SM_CYEDGE,
            'cxminimizedspacing': win32con.SM_CXMINIMIZEDSPACING,
            'cyminimizedspacing': win32con.SM_CYMINIMIZEDSPACING,
            'cxvscroll': win32con.SM_CXVSCROLL,
            'cyhscroll': win32con.SM_CYHSCROLL,
            'show_buttons': win32con.SM_SHOWSOUNDS,
            'cxscreensize': win32con.SM_CXSCREEN,
            'cyscreensize': win32con.SM_CYSCREEN
        }
        
        if isinstance(index, str) and index in metrics:
            return win32api.GetSystemMetrics(metrics[index])
        return win32api.GetSystemMetrics(index)
    
    def get_screen_size(self):
        """Ukuran layar [width, height]"""
        if not self.is_available: return [0, 0]
        return [
            win32api.GetSystemMetrics(win32con.SM_CXSCREEN),
            win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        ]
    
    def get_work_area(self):
        """Area kerja (tanpa taskbar) [left, top, right, bottom]"""
        if not self.is_available: return [0, 0, 0, 0]
        rect = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0,0)))['Work']
        return list(rect)
    
    def get_monitors(self):
        """Daftar semua monitor"""
        if not self.is_available: return []
        monitors = []
        
        def callback(hmonitor, hdc, rect, param):
            info = win32api.GetMonitorInfo(hmonitor)
            monitors.append({
                'handle': hmonitor,
                'rect': list(info['Monitor']),
                'work': list(info['Work']),
                'primary': info.get('Flags', 0) == 1
            })
            return True
        
        win32api.EnumDisplayMonitors(None, None, callback, None)
        return monitors
    
    # ========== PROSES DAN THREAD ==========
    def process_start(self, filename, args="", show=1):
        """Jalankan proses baru"""
        if not self.is_available: return 0
        try:
            si = win32process.STARTUPINFO()
            si.dwFlags = win32con.STARTF_USESHOWWINDOW
            si.wShowWindow = show
            
            handle, thread_id, pid, thread_handle = win32process.CreateProcess(
                filename, args, None, None, 0,
                win32con.NORMAL_PRIORITY_CLASS, None, None, si
            )
            return pid
        except Exception as e:
            print(f"Process start error: {e}")
            return 0
    
    def process_kill(self, pid):
        """Hentikan proses berdasarkan PID"""
        if not self.is_available: return False
        try:
            handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, False, pid)
            win32api.TerminateProcess(handle, 0)
            win32api.CloseHandle(handle)
            return True
        except:
            return False
    
    def process_kill_by_name(self, name):
        """Hentikan semua proses dengan nama tertentu"""
        if not self.is_available: return 0
        killed = 0
        for proc in self.process_list():
            if proc['name'].lower() == name.lower():
                if self.process_kill(proc['pid']):
                    killed += 1
        return killed
    
    def process_exists(self, pid):
        """Cek apakah proses dengan PID masih berjalan"""
        if not self.is_available: return False
        try:
            handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION, False, pid)
            win32api.CloseHandle(handle)
            return True
        except:
            return False
    
    def process_list(self):
        """Daftar semua proses berjalan"""
        if not self.is_available: return []
        processes = []
        
        try:
            import psutil
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                processes.append(proc.info)
        except ImportError:
            # Fallback menggunakan pdh
            try:
                hq = win32pdh.OpenQuery()
                # Implementasi PDH cukup kompleks, fallback simple
                pass
            except:
                pass
        
        return processes
    
    def process_get_memory(self, pid):
        """Memory usage proses dalam bytes"""
        if not self.is_available: return 0
        try:
            handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, pid)
            memory = win32process.GetProcessMemoryInfo(handle)
            win32api.CloseHandle(handle)
            return memory['WorkingSetSize']
        except:
            return 0
    
    def process_get_cpu(self, pid):
        """CPU usage proses"""
        if not self.is_available: return 0.0
        try:
            import psutil
            return psutil.Process(pid).cpu_percent()
        except:
            return 0.0
    
    def process_wait(self, pid, timeout=win32event.INFINITE):
        """Tunggu proses selesai"""
        if not self.is_available: return False
        try:
            handle = win32api.OpenProcess(win32con.SYNCHRONIZE, False, pid)
            result = win32event.WaitForSingleObject(handle, timeout)
            win32api.CloseHandle(handle)
            return result == 0
        except:
            return False
    
    def thread_get_current(self):
        """Dapatkan ID thread saat ini"""
        if not self.is_available: return 0
        return win32api.GetCurrentThreadId()
    
    def thread_get_current_process(self):
        """Dapatkan ID proses saat ini"""
        if not self.is_available: return 0
        return win32api.GetCurrentProcessId()
    
    def thread_get_current_process_handle(self):
        """Dapatkan handle proses saat ini"""
        if not self.is_available: return 0
        return win32api.GetCurrentProcess()
    
    # ========== WINDOW MANAGEMENT ==========
    def find_window(self, class_name=None, title=None):
        """Cari window handle berdasarkan class name atau title"""
        if not self.is_available: return 0
        return win32gui.FindWindow(class_name, title)
    
    def find_window_ex(self, parent, class_name, title):
        """Cari window child"""
        if not self.is_available: return 0
        return win32gui.FindWindowEx(parent, 0, class_name, title)
    
    def get_window_text(self, hwnd):
        """Ambil teks/judul window"""
        if not self.is_available: return ""
        return win32gui.GetWindowText(hwnd)
    
    def get_window_class(self, hwnd):
        """Ambil class name window"""
        if not self.is_available: return ""
        return win32gui.GetClassName(hwnd)
    
    def get_window_rect(self, hwnd):
        """Ambil posisi dan ukuran window [left, top, right, bottom]"""
        if not self.is_available: return [0, 0, 0, 0]
        rect = win32gui.GetWindowRect(hwnd)
        return list(rect)
    
    def get_window_size(self, hwnd):
        """Ambil ukuran window [width, height]"""
        if not self.is_available: return [0, 0]
        rect = win32gui.GetWindowRect(hwnd)
        return [rect[2] - rect[0], rect[3] - rect[1]]
    
    def get_window_position(self, hwnd):
        """Ambil posisi window [x, y]"""
        if not self.is_available: return [0, 0]
        rect = win32gui.GetWindowRect(hwnd)
        return [rect[0], rect[1]]
    
    def set_window_pos(self, hwnd, x, y, width, height):
        """Set posisi dan ukuran window"""
        if not self.is_available: return False
        win32gui.SetWindowPos(hwnd, 0, x, y, width, height, 0)
        return True
    
    def set_window_text(self, hwnd, text):
        """Set teks/judul window"""
        if not self.is_available: return False
        win32gui.SetWindowText(hwnd, text)
        return True
    
    def show_window(self, hwnd, cmd=win32con.SW_SHOW):
        """Tampilkan/sembunyikan window"""
        if not self.is_available: return False
        win32gui.ShowWindow(hwnd, cmd)
        return True
    
    def hide_window(self, hwnd):
        """Sembunyikan window"""
        return self.show_window(hwnd, win32con.SW_HIDE)
    
    def minimize_window(self, hwnd):
        """Minimize window"""
        return self.show_window(hwnd, win32con.SW_MINIMIZE)
    
    def maximize_window(self, hwnd):
        """Maximize window"""
        return self.show_window(hwnd, win32con.SW_MAXIMIZE)
    
    def restore_window(self, hwnd):
        """Restore window dari minimized/maximized"""
        return self.show_window(hwnd, win32con.SW_RESTORE)
    
    def close_window(self, hwnd):
        """Tutup window (kirim WM_CLOSE)"""
        if not self.is_available: return False
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        return True
    
    def destroy_window(self, hwnd):
        """Hancurkan window paksa"""
        if not self.is_available: return False
        win32gui.DestroyWindow(hwnd)
        return True
    
    def set_window_topmost(self, hwnd, enable=True):
        """Set window selalu di atas"""
        if not self.is_available: return False
        if enable:
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, 
                                  win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        else:
            win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                                  win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        return True
    
    def set_window_foreground(self, hwnd):
        """Set window sebagai foreground"""
        if not self.is_available: return False
        win32gui.SetForegroundWindow(hwnd)
        return True
    
    def flash_window(self, hwnd, count=3):
        """Buat window berkedip di taskbar"""
        if not self.is_available: return False
        win32gui.FlashWindow(hwnd, True)
        return True
    
    def enum_windows(self):
        """Daftar semua window top-level"""
        if not self.is_available: return []
        windows = []
        
        def callback(hwnd, param):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title:  # Hanya window dengan title
                    windows.append({
                        'handle': hwnd,
                        'title': title,
                        'class': win32gui.GetClassName(hwnd),
                        'rect': list(win32gui.GetWindowRect(hwnd))
                    })
            return True
        
        win32gui.EnumWindows(callback, None)
        return windows
    
    def enum_child_windows(self, hwnd):
        """Daftar semua child window dari suatu window"""
        if not self.is_available: return []
        windows = []
        
        def callback(child_hwnd, param):
            windows.append({
                'handle': child_hwnd,
                'title': win32gui.GetWindowText(child_hwnd),
                'class': win32gui.GetClassName(child_hwnd)
            })
            return True
        
        win32gui.EnumChildWindows(hwnd, callback, None)
        return windows
    
    def get_active_window(self):
        """Dapatkan window yang sedang aktif"""
        if not self.is_available: return 0
        return win32gui.GetForegroundWindow()
    
    def get_desktop_window(self):
        """Dapatkan desktop window"""
        if not self.is_available: return 0
        return win32gui.GetDesktopWindow()
    
    def get_shell_window(self):
        """Dapatkan shell window (explorer)"""
        if not self.is_available: return 0
        return win32gui.GetShellWindow()
    
    def window_from_point(self, x, y):
        """Cari window pada koordinat tertentu"""
        if not self.is_available: return 0
        return win32gui.WindowFromPoint((x, y))
    
    # ========== MESSAGE BOX DAN DIALOG ==========
    def msgbox(self, text, title="JPX", type="info"):
        """Message box dengan berbagai tipe"""
        if not self.is_available:
            print(f"[{title}] {text}")
            return win32con.IDOK
        
        flags_map = {
            "info": win32con.MB_OK | win32con.MB_ICONINFORMATION,
            "warn": win32con.MB_OK | win32con.MB_ICONWARNING,
            "error": win32con.MB_OK | win32con.MB_ICONERROR,
            "question": win32con.MB_OK | win32con.MB_ICONQUESTION,
            "yesno": win32con.MB_YESNO | win32con.MB_ICONQUESTION,
            "yesnocancel": win32con.MB_YESNOCANCEL | win32con.MB_ICONQUESTION,
            "okcancel": win32con.MB_OKCANCEL | win32con.MB_ICONQUESTION,
            "retrycancel": win32con.MB_RETRYCANCEL | win32con.MB_ICONWARNING,
            "abortretryignore": win32con.MB_ABORTRETRYIGNORE | win32con.MB_ICONWARNING
        }
        
        flags = flags_map.get(type, win32con.MB_OK)
        return win32api.MessageBox(0, text, title, flags)
    
    def msgbox_yesno(self, text, title="JPX"):
        """Message box Yes/No"""
        return self.msgbox(text, title, "yesno")
    
    def msgbox_okcancel(self, text, title="JPX"):
        """Message box OK/Cancel"""
        return self.msgbox(text, title, "okcancel")
    
    def msgbox_yesnocancel(self, text, title="JPX"):
        """Message box Yes/No/Cancel"""
        return self.msgbox(text, title, "yesnocancel")
    
    def msgbox_retrycancel(self, text, title="JPX"):
        """Message box Retry/Cancel"""
        return self.msgbox(text, title, "retrycancel")
    
    def inputbox(self, prompt, title="JPX", default=""):
        """Input box menggunakan COM"""
        if not self.is_available:
            return input(f"{prompt}: ")
        
        try:
            shell = win32com.client.Dispatch("WScript.Shell")
            return shell.Popup(prompt, 0, title, 0, default)
        except:
            return input(f"{prompt}: ")
    
    def file_open_dialog(self, title="Buka File", filter="All Files|*.*", start_dir=""):
        """Dialog buka file"""
        if not self.is_available: return ""
        
        import win32ui
        dlg = win32ui.CreateFileDialog(1, None, None, 0, filter, None)
        dlg.SetOFNTitle(title)
        if start_dir:
            dlg.SetOFNInitialDir(start_dir)
        
        if dlg.DoModal() == win32con.IDOK:
            return dlg.GetPathName()
        return ""
    
    def file_save_dialog(self, title="Simpan File", filter="All Files|*.*", start_dir=""):
        """Dialog simpan file"""
        if not self.is_available: return ""
        
        import win32ui
        dlg = win32ui.CreateFileDialog(0, None, None, 0, filter, None)
        dlg.SetOFNTitle(title)
        if start_dir:
            dlg.SetOFNInitialDir(start_dir)
        
        if dlg.DoModal() == win32con.IDOK:
            return dlg.GetPathName()
        return ""
    
    def folder_dialog(self, title="Pilih Folder", start_dir=""):
        """Dialog pilih folder"""
        if not self.is_available: return ""
        
        import win32ui
        from win32com.shell import shell, shellcon
        
        pidl, display, _ = shell.SHBrowseForFolder(
            win32ui.GetMainFrame().GetSafeHwnd(),
            None,
            title,
            shellcon.BIF_RETURNONLYFSDIRS | shellcon.BIF_NEWDIALOGSTYLE,
            None,
            None
        )
        
        if pidl:
            return shell.SHGetPathFromIDList(pidl)
        return ""
    
    def color_dialog(self, title="Pilih Warna", default_color=0):
        """Dialog pilih warna"""
        if not self.is_available: return 0
        
        import win32ui
        dlg = win32ui.CreateColorDialog(default_color, 0, None)
        if dlg.DoModal() == win32con.IDOK:
            return dlg.GetColor()
        return default_color
    
    def font_dialog(self, title="Pilih Font"):
        """Dialog pilih font"""
        if not self.is_available: return None
        
        import win32ui
        dlg = win32ui.CreateFontDialog(None, 0, None)
        if dlg.DoModal() == win32con.IDOK:
            return {
                'name': dlg.GetFaceName(),
                'size': dlg.GetPointSize(),
                'bold': dlg.IsBold(),
                'italic': dlg.IsItalic(),
                'underline': dlg.IsUnderline(),
                'strike': dlg.IsStrikeOut()
            }
        return None
    
    # ========== CLIPBOARD ==========
    def clipboard_set(self, text):
        """Copy teks ke clipboard"""
        if not self.is_available: return False
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
            return True
        except:
            return False
    
    def clipboard_get(self):
        """Paste teks dari clipboard"""
        if not self.is_available: return ""
        try:
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
            return data
        except:
            return ""
    
    def clipboard_clear(self):
        """Bersihkan clipboard"""
        if not self.is_available: return False
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.CloseClipboard()
            return True
        except:
            return False
    
    def clipboard_set_files(self, files):
        """Copy file ke clipboard"""
        if not self.is_available: return False
        try:
            import win32clipboard
            import win32con
            from win32com.shell import shell, shellcon
            
            # Format HDROP untuk file
            # Implementasi kompleks, fallback
            return False
        except:
            return False
    
    def clipboard_get_files(self):
        """Paste file dari clipboard"""
        if not self.is_available: return []
        # Implementasi kompleks
        return []
    
    def clipboard_set_image(self, image_path):
        """Copy gambar ke clipboard"""
        if not self.is_available: return False
        # Implementasi kompleks
        return False
    
    def clipboard_get_formats(self):
        """Daftar format yang tersedia di clipboard"""
        if not self.is_available: return []
        formats = []
        try:
            win32clipboard.OpenClipboard()
            fmt = win32clipboard.EnumClipboardFormats(0)
            while fmt:
                formats.append(fmt)
                fmt = win32clipboard.EnumClipboardFormats(fmt)
            win32clipboard.CloseClipboard()
        except:
            pass
        return formats
    
    # ========== REGISTRY ==========
    def reg_read(self, key, subkey, value):
        """Baca value dari registry"""
        if not self.is_available: return None
        import win32reg
        
        key_map = {
            'HKCR': win32reg.HKEY_CLASSES_ROOT,
            'HKCU': win32reg.HKEY_CURRENT_USER,
            'HKLM': win32reg.HKEY_LOCAL_MACHINE,
            'HKU': win32reg.HKEY_USERS,
            'HKCC': win32reg.HKEY_CURRENT_CONFIG
        }
        
        if isinstance(key, str):
            key = key_map.get(key.upper(), win32reg.HKEY_CURRENT_USER)
        
        try:
            handle = win32reg.OpenKey(key, subkey)
            data, type = win32reg.QueryValueEx(handle, value)
            win32reg.CloseKey(handle)
            return data
        except:
            return None
    
    def reg_write(self, key, subkey, value, data, type=win32reg.REG_SZ):
        """Tulis value ke registry"""
        if not self.is_available: return False
        import win32reg
        
        key_map = {
            'HKCR': win32reg.HKEY_CLASSES_ROOT,
            'HKCU': win32reg.HKEY_CURRENT_USER,
            'HKLM': win32reg.HKEY_LOCAL_MACHINE,
            'HKU': win32reg.HKEY_USERS,
            'HKCC': win32reg.HKEY_CURRENT_CONFIG
        }
        
        if isinstance(key, str):
            key = key_map.get(key.upper(), win32reg.HKEY_CURRENT_USER)
        
        try:
            handle = win32reg.OpenKey(key, subkey, 0, win32reg.KEY_WRITE)
            win32reg.SetValueEx(handle, value, 0, type, data)
            win32reg.CloseKey(handle)
            return True
        except:
            try:
                handle = win32reg.CreateKey(key, subkey)
                win32reg.SetValueEx(handle, value, 0, type, data)
                win32reg.CloseKey(handle)
                return True
            except:
                return False
    
    def reg_delete(self, key, subkey, value=None):
        """Hapus key atau value dari registry"""
        if not self.is_available: return False
        import win32reg
        
        key_map = {
            'HKCR': win32reg.HKEY_CLASSES_ROOT,
            'HKCU': win32reg.HKEY_CURRENT_USER,
            'HKLM': win32reg.HKEY_LOCAL_MACHINE,
            'HKU': win32reg.HKEY_USERS,
            'HKCC': win32reg.HKEY_CURRENT_CONFIG
        }
        
        if isinstance(key, str):
            key = key_map.get(key.upper(), win32reg.HKEY_CURRENT_USER)
        
        try:
            if value:
                handle = win32reg.OpenKey(key, subkey, 0, win32reg.KEY_WRITE)
                win32reg.DeleteValue(handle, value)
                win32reg.CloseKey(handle)
            else:
                win32reg.DeleteKey(key, subkey)
            return True
        except:
            return False
    
    def reg_list_keys(self, key, subkey):
        """Daftar subkey di registry"""
        if not self.is_available: return []
        import win32reg
        
        key_map = {
            'HKCR': win32reg.HKEY_CLASSES_ROOT,
            'HKCU': win32reg.HKEY_CURRENT_USER,
            'HKLM': win32reg.HKEY_LOCAL_MACHINE,
            'HKU': win32reg.HKEY_USERS,
            'HKCC': win32reg.HKEY_CURRENT_CONFIG
        }
        
        if isinstance(key, str):
            key = key_map.get(key.upper(), win32reg.HKEY_CURRENT_USER)
        
        keys = []
        try:
            handle = win32reg.OpenKey(key, subkey)
            i = 0
            while True:
                try:
                    name = win32reg.EnumKey(handle, i)
                    keys.append(name)
                    i += 1
                except:
                    break
            win32reg.CloseKey(handle)
        except:
            pass
        return keys
    
    def reg_list_values(self, key, subkey):
        """Daftar values di registry key"""
        if not self.is_available: return []
        import win32reg
        
        key_map = {
            'HKCR': win32reg.HKEY_CLASSES_ROOT,
            'HKCU': win32reg.HKEY_CURRENT_USER,
            'HKLM': win32reg.HKEY_LOCAL_MACHINE,
            'HKU': win32reg.HKEY_USERS,
            'HKCC': win32reg.HKEY_CURRENT_CONFIG
        }
        
        if isinstance(key, str):
            key = key_map.get(key.upper(), win32reg.HKEY_CURRENT_USER)
        
        values = []
        try:
            handle = win32reg.OpenKey(key, subkey)
            i = 0
            while True:
                try:
                    name, data, type = win32reg.EnumValue(handle, i)
                    values.append({'name': name, 'data': data, 'type': type})
                    i += 1
                except:
                    break
            win32reg.CloseKey(handle)
        except:
            pass
        return values
    
    # ========== FILE SYSTEM ==========
    def get_drives(self):
        """Daftar semua drive"""
        if not self.is_available: return []
        drives = []
        for i in range(65, 91):
            drive = chr(i) + ":\\"
            if os.path.exists(drive):
                drives.append(drive)
        return drives
    
    def get_drive_type(self, drive):
        """Tipe drive"""
        if not self.is_available: return "unknown"
        types = {
            win32con.DRIVE_UNKNOWN: "unknown",
            win32con.DRIVE_NO_ROOT_DIR: "invalid",
            win32con.DRIVE_REMOVABLE: "removable",
            win32con.DRIVE_FIXED: "fixed",
            win32con.DRIVE_REMOTE: "network",
            win32con.DRIVE_CDROM: "cdrom",
            win32con.DRIVE_RAMDISK: "ramdisk"
        }
        drive_type = win32file.GetDriveType(drive)
        return types.get(drive_type, "unknown")
    
    def get_disk_free(self, path):
        """Free space dalam bytes"""
        if not self.is_available: return 0
        try:
            _, free, _ = win32file.GetDiskFreeSpaceEx(path)
            return free
        except:
            return 0
    
    def get_disk_total(self, path):
        """Total space dalam bytes"""
        if not self.is_available: return 0
        try:
            total, _, _ = win32file.GetDiskFreeSpaceEx(path)
            return total
        except:
            return 0
    
    def get_disk_used(self, path):
        """Used space dalam bytes"""
        if not self.is_available: return 0
        try:
            total, free, _ = win32file.GetDiskFreeSpaceEx(path)
            return total - free
        except:
            return 0
    
    def get_disk_info(self, path):
        """Informasi lengkap disk"""
        if not self.is_available: return {}
        try:
            total, free, _ = win32file.GetDiskFreeSpaceEx(path)
            secPerClus, bytesPerSec, freeClus, totalClus = win32file.GetDiskFreeSpace(path)
            return {
                'total': total,
                'free': free,
                'used': total - free,
                'total_clusters': totalClus,
                'free_clusters': freeClus,
                'sectors_per_cluster': secPerClus,
                'bytes_per_sector': bytesPerSec,
                'bytes_per_cluster': secPerClus * bytesPerSec
            }
        except:
            return {}
    
    def get_volume_info(self, drive):
        """Informasi volume"""
        if not self.is_available: return {}
        try:
            name, serial, maxlen, flags, fs = win32file.GetVolumeInformation(drive)
            return {
                'name': name,
                'serial': serial,
                'max_component_length': maxlen,
                'flags': flags,
                'filesystem': fs
            }
        except:
            return {}
    
    def get_file_attributes(self, path):
        """Attributes file"""
        if not self.is_available: return 0
        try:
            return win32file.GetFileAttributes(path)
        except:
            return 0
    
    def set_file_attributes(self, path, attrs):
        """Set attributes file"""
        if not self.is_available: return False
        try:
            win32file.SetFileAttributes(path, attrs)
            return True
        except:
            return False
    
    def get_file_time(self, path):
        """Waktu file (created, accessed, modified)"""
        if not self.is_available: return {}
        try:
            handle = win32file.CreateFile(
                path, win32file.GENERIC_READ,
                win32file.FILE_SHARE_READ, None,
                win32file.OPEN_EXISTING, 0, None
            )
            ctime, atime, mtime = win32file.GetFileTime(handle)
            win32file.CloseHandle(handle)
            
            # Convert ke timestamp
            import time
            return {
                'created': time.mktime(ctime.timetuple()) if ctime else 0,
                'accessed': time.mktime(atime.timetuple()) if atime else 0,
                'modified': time.mktime(mtime.timetuple()) if mtime else 0
            }
        except:
            return {}
    
    # ========== NETWORK ==========
    def get_computer_name(self):
        return win32api.GetComputerName()
    
    def get_user_name(self):
        return win32api.GetUserName()
    
    def get_domain_name(self):
        """Nama domain komputer"""
        if not self.is_available: return ""
        try:
            return win32api.GetComputerNameEx(win32con.ComputerNameDnsDomain)
        except:
            return ""
    
    def ping(self, host):
        """Ping host"""
        if not self.is_available: return False
        try:
            response = os.system(f"ping -n 1 -w 1000 {host} > nul")
            return response == 0
        except:
            return False
    
    def get_ip_address(self):
        """IP address lokal"""
        if not self.is_available: return ""
        try:
            hostname = win32api.GetComputerName()
            return win32net.NetworkNameFromComputerName(hostname)
        except:
            return ""
    
    def get_mac_address(self):
        """MAC address"""
        if not self.is_available: return ""
        try:
            import uuid
            return ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) 
                            for ele in range(0, 8*6, 8)][::-1])
        except:
            return ""
    
    def net_share_list(self, computer=None):
        """Daftar shared folder"""
        if not self.is_available: return []
        try:
            shares = []
            resume = 0
            while True:
                data, total, resume = win32net.NetShareEnum(
                    computer or None, 2, resume
                )
                if not data:
                    break
                shares.extend(data)
            return shares
        except:
            return []
    
    def net_connection_list(self):
        """Daftar koneksi jaringan"""
        if not self.is_available: return []
        try:
            return win32net.NetConnectionEnum(None, None, 0)
        except:
            return []
    
    def net_use(self, remote, local=None, user=None, password=None):
        """Map network drive"""
        if not self.is_available: return False
        try:
            params = {
                'remote': remote,
                'local': local or '',
                'username': user or '',
                'password': password or ''
            }
            win32wnet.WNetAddConnection2(params)
            return True
        except:
            return False
    
    def net_use_delete(self, local):
        """Unmap network drive"""
        if not self.is_available: return False
        try:
            win32wnet.WNetCancelConnection2(local, 0, True)
            return True
        except:
            return False
    
    # ========== SERVICE MANAGEMENT ==========
    def service_list(self):
        """Daftar semua services"""
        if not self.is_available: return []
        try:
            return win32service.EnumServicesStatus(
                win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ALL_ACCESS)
            )
        except:
            return []
    
    def service_start(self, name):
        """Start service"""
        if not self.is_available: return False
        try:
            win32serviceutil.StartService(name)
            return True
        except:
            return False
    
    def service_stop(self, name):
        """Stop service"""
        if not self.is_available: return False
        try:
            win32serviceutil.StopService(name)
            return True
        except:
            return False
    
    def service_restart(self, name):
        """Restart service"""
        if not self.is_available: return False
        try:
            win32serviceutil.RestartService(name)
            return True
        except:
            return False
    
    def service_status(self, name):
        """Status service"""
        if not self.is_available: return ""
        try:
            status = win32serviceutil.QueryServiceStatus(name)
            return status[1]  # Current state
        except:
            return ""
    
    # ========== POWER MANAGEMENT ==========
    def shutdown(self, force=False):
        """Shutdown komputer"""
        if not self.is_available: return False
        try:
            flags = win32con.SHTDN_REASON_MAJOR_OTHER
            if force:
                flags |= win32con.SHUTDOWN_FORCE_OTHERS
            win32api.InitiateSystemShutdown(None, None, 0, force, True)
            return True
        except:
            return False
    
    def reboot(self, force=False):
        """Restart komputer"""
        if not self.is_available: return False
        try:
            flags = win32con.SHTDN_REASON_MAJOR_OTHER
            if force:
                flags |= win32con.SHUTDOWN_FORCE_OTHERS
            win32api.InitiateSystemShutdown(None, None, 0, force, False)
            return True
        except:
            return False
    
    def logout(self, force=False):
        """Logout user"""
        if not self.is_available: return False
        try:
            win32api.ExitWindowsEx(win32con.EWX_LOGOFF | (win32con.EWX_FORCE if force else 0), 0)
            return True
        except:
            return False
    
    def suspend(self):
        """Sleep mode"""
        if not self.is_available: return False
        try:
            win32api.SetSuspendState(False, True, False)
            return True
        except:
            return False
    
    def hibernate(self):
        """Hibernate mode"""
        if not self.is_available: return False
        try:
            win32api.SetSuspendState(True, True, False)
            return True
        except:
            return False
    
    def lock(self):
        """Lock workstation"""
        if not self.is_available: return False
        try:
            win32api.LockWorkStation()
            return True
        except:
            return False
    
    def get_last_input(self):
        """Waktu sejak input terakhir (idle time)"""
        if not self.is_available: return 0
        try:
            last_input = win32api.GetLastInputInfo()
            return win32api.GetTickCount() - last_input
        except:
            return 0
    
    # ========== PRINTING ==========
    def printer_get_default(self):
        """Printer default"""
        if not self.is_available: return ""
        return win32print.GetDefaultPrinter()
    
    def printer_list(self):
        """Daftar semua printer"""
        if not self.is_available: return []
        return win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
    
    def printer_get_info(self, name):
        """Informasi printer"""
        if not self.is_available: return {}
        try:
            handle = win32print.OpenPrinter(name)
            info = win32print.GetPrinter(handle, 2)
            win32print.ClosePrinter(handle)
            return info
        except:
            return {}
    
    def printer_set_default(self, name):
        """Set printer default"""
        if not self.is_available: return False
        try:
            win32print.SetDefaultPrinter(name)
            return True
        except:
            return False
    
    def print_file(self, filename, printer=None):
        """Print file"""
        if not self.is_available: return False
        try:
            if printer:
                win32api.ShellExecute(0, "print", filename, None, ".", 0)
            else:
                win32api.ShellExecute(0, "print", filename, f'/d:"{printer}"', ".", 0)
            return True
        except:
            return False
    
    # ========== ENVIRONMENT VARIABLES ==========
    def env_get(self, name):
        """Get environment variable"""
        return os.environ.get(name, "")
    
    def env_set(self, name, value):
        """Set environment variable"""
        os.environ[name] = value
        return True
    
    def env_delete(self, name):
        """Delete environment variable"""
        if name in os.environ:
            del os.environ[name]
            return True
        return False
    
    def env_list(self):
        """List all environment variables"""
        return list(os.environ.keys())
    
    # ========== MISC ==========
    def beep(self, freq=1000, duration=500):
        """Bunyi beep"""
        if not self.is_available: return False
        try:
            import winsound
            winsound.Beep(freq, duration)
            return True
        except:
            return False
    
    def get_tick_count(self):
        """Waktu sejak Windows start (ms)"""
        if not self.is_available: return 0
        return win32api.GetTickCount()
    
    def get_last_error(self):
        """Error terakhir"""
        if not self.is_available: return 0
        return win32api.GetLastError()
    
    def format_message(self, error_code):
        """Format pesan error"""
        if not self.is_available: return ""
        return win32api.FormatMessage(error_code)
    
    def open_with(self, filename, app=None):
        """Buka file dengan aplikasi tertentu"""
        if not self.is_available: return False
        try:
            if app:
                win32api.ShellExecute(0, "open", app, filename, None, 1)
            else:
                win32api.ShellExecute(0, "open", filename, None, None, 1)
            return True
        except:
            return False
    
    def explore(self, path):
        """Buka Windows Explorer di path tertentu"""
        if not self.is_available: return False
        try:
            win32api.ShellExecute(0, "explore", path, None, None, 1)
            return True
        except:
            return False
    
    def get_special_folder(self, folder_id):
        """Dapatkan path special folder (Desktop, Documents, etc)"""
        if not self.is_available: return ""
        try:
            from win32com.shell import shell, shellcon
            return shell.SHGetFolderPath(0, folder_id, 0, 0)
        except:
            return ""
    
    def get_desktop(self):
        """Path desktop"""
        return self.get_special_folder(shellcon.CSIDL_DESKTOP)
    
    def get_documents(self):
        """Path documents"""
        return self.get_special_folder(shellcon.CSIDL_PERSONAL)
    
    def get_appdata(self):
        """Path AppData"""
        return self.get_special_folder(shellcon.CSIDL_APPDATA)
    
    def get_local_appdata(self):
        """Path Local AppData"""
        return self.get_special_folder(shellcon.CSIDL_LOCAL_APPDATA)
    
    def get_startup(self):
        """Path Startup folder"""
        return self.get_special_folder(shellcon.CSIDL_STARTUP)
    
    def get_temp(self):
        """Path temp folder"""
        return os.environ.get('TEMP', os.environ.get('TMP', ''))
    
    def get_programs(self):
        """Path Programs folder"""
        return self.get_special_folder(shellcon.CSIDL_PROGRAMS)

# Ekspor instance win32
exports = {
    'win32': Win32()
}