"""
win32ui.py - UI Windows klasik menggunakan pywin32
Sudah terbukti stabil dan tidak ada masalah threading
"""

import sys
import os
import win32api
import win32con
import win32gui
import win32ui
from pywin.mfc import dialog
import commctrl
import win32com.client

class Win32UI:
    def __init__(self):
        self.windows = {}
        self.next_id = 1000
    
    def Dialog(self, title="JPX Dialog", width=400, height=300):
        """Buat dialog/window sederhana"""
        dlg = JpxDialog(title, width, height)
        dlg_id = id(dlg)
        self.windows[dlg_id] = dlg
        return dlg
    
    def MessageBox(self, text, title="JPX", type="info"):
        """Message box"""
        flags = {
            "info": win32con.MB_OK | win32con.MB_ICONINFORMATION,
            "warn": win32con.MB_OK | win32con.MB_ICONWARNING,
            "error": win32con.MB_OK | win32con.MB_ICONERROR,
            "yesno": win32con.MB_YESNO | win32con.MB_ICONQUESTION,
            "okcancel": win32con.MB_OKCANCEL | win32con.MB_ICONQUESTION
        }
        flag = flags.get(type, win32con.MB_OK)
        return win32api.MessageBox(0, text, title, flag)

class JpxDialog(dialog.Dialog):
    def __init__(self, title, width, height):
        style = win32con.WS_OVERLAPPED | win32con.WS_CAPTION | win32con.WS_SYSMENU | win32con.WS_VISIBLE
        self.width = width
        self.height = height
        self.title = title
        self.controls = {}
        self.callbacks = {}
        self.next_control_id = 2000
        
        # Template dialog
        template = [
            [title, (0, 0, width, height), style, None, (8, "MS Sans Serif")],
        ]
        dialog.Dialog.__init__(self, template)
    
    def OnInitDialog(self):
        """Inisialisasi dialog"""
        # Set posisi di tengah layar
        self.CenterWindow()
        return True
    
    def OnClose(self):
        self.EndDialog(0)
    
    def _next_id(self):
        self.next_control_id += 1
        return self.next_control_id
    
    # ========== CONTROLS ==========
    
    def Button(self, text, x, y, width=80, height=25, callback=None):
        """Tambah tombol"""
        cid = self._next_id()
        self.ButtonADD(cid, text, x, y, width, height)
        if callback:
            self.callbacks[cid] = callback
        return cid
    
    def Label(self, text, x, y, width=100, height=20):
        """Tambah label"""
        cid = self._next_id()
        self.StaticText(text, cid, x, y, width, height)
        return cid
    
    def TextBox(self, x, y, width=200, height=25, text=""):
        """Tambah textbox"""
        cid = self._next_id()
        self.Edit(text, cid, x, y, width, height, win32con.ES_AUTOHSCROLL)
        return cid
    
    def CheckBox(self, text, x, y, width=120, height=20, checked=False):
        """Tambah checkbox"""
        cid = self._next_id()
        style = win32con.BS_AUTOCHECKBOX | win32con.WS_TABSTOP
        self.Button(text, cid, style, x, y, width, height)
        if checked:
            self.CheckDlgButton(cid, 1)
        return cid
    
    def RadioButton(self, text, x, y, width=120, height=20, group=False):
        """Tambah radio button"""
        cid = self._next_id()
        style = win32con.BS_AUTORADIOBUTTON | win32con.WS_TABSTOP
        if group:
            style |= win32con.WS_GROUP
        self.Button(text, cid, style, x, y, width, height)
        return cid
    
    def ComboBox(self, x, y, width=200, height=25, items=[]):
        """Tambah combobox"""
        cid = self._next_id()
        style = win32con.CBS_DROPDOWNLIST | win32con.WS_VSCROLL | win32con.WS_TABSTOP
        self.MakeComboBox(style, cid, x, y, width, height * 5)
        for item in items:
            self.SendDlgItemMessage(cid, win32con.CB_ADDSTRING, 0, item)
        return cid
    
    def ListBox(self, x, y, width=200, height=100, items=[]):
        """Tambah listbox"""
        cid = self._next_id()
        style = win32con.LBS_NOTIFY | win32con.WS_VSCROLL | win32con.WS_TABSTOP
        self.MakeListBox(style, cid, x, y, width, height)
        for item in items:
            self.SendDlgItemMessage(cid, win32con.LB_ADDSTRING, 0, item)
        return cid
    
    def ProgressBar(self, x, y, width=200, height=20):
        """Tambah progress bar"""
        from pywin.mfc import window
        cid = self._next_id()
        
        # Buat progress bar
        prog = window.CreateWindow(
            commctrl.PROGRESS_CLASS,
            "",
            win32con.WS_VISIBLE | win32con.WS_CHILD,
            (x, y, width, height),
            self.GetWindow(),
            cid
        )
        prog.SendMessage(commctrl.PBM_SETRANGE, 0, 100)
        self.controls[cid] = prog
        return cid
    
    # ========== GET/SET VALUES ==========
    
    def GetText(self, cid):
        """Ambil teks dari kontrol"""
        return self.GetDlgItemText(cid)
    
    def SetText(self, cid, text):
        """Set teks ke kontrol"""
        self.SetDlgItemText(cid, text)
    
    def GetChecked(self, cid):
        """Ambil status checkbox/radio"""
        return self.IsDlgButtonChecked(cid)
    
    def SetChecked(self, cid, checked):
        """Set status checkbox/radio"""
        self.CheckDlgButton(cid, 1 if checked else 0)
    
    def GetSelect(self, cid):
        """Ambil item yang dipilih di combobox/listbox"""
        sel = self.SendDlgItemMessage(cid, win32con.CB_GETCURSEL)
        if sel >= 0:
            return self.SendDlgItemMessage(cid, win32con.CB_GETLBTEXT, sel)
        return None
    
    def SetProgress(self, cid, value):
        """Set nilai progress bar"""
        if cid in self.controls:
            self.controls[cid].SendMessage(commctrl.PBM_SETPOS, value)
    
    # ========== EVENTS ==========
    
    def OnCommand(self, hwnd, msg, wparam, lparam):
        """Handle command messages"""
        cid = wparam & 0xFFFF
        code = (wparam >> 16) & 0xFFFF
        
        # Button click
        if code == 0 and cid in self.callbacks:
            self.callbacks[cid]()
        
        # Combo/List selection
        elif code in [win32con.CBN_SELCHANGE, win32con.LBN_SELCHANGE] and cid in self.callbacks:
            self.callbacks[cid]()
        
        return 1

# ========== MODULE EXPORTS ==========
exports = {
    'win32ui': Win32UI()
}