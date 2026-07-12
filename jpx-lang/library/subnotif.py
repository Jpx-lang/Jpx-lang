"""
notification.py - Modul notifikasi Windows dengan PowerShell
Error handling lengkap dan fallback ke console
"""

import subprocess
import platform
import sys
import os
import tempfile

class Notification:
    def __init__(self):
        self.is_windows = platform.system() == "Windows"
        self.last_error = None
        self.debug_mode = False
    
    def _debug(self, msg):
        """Internal debug"""
        if self.debug_mode:
            print(f"[DEBUG] {msg}")
    
    def _check_windows(self):
        """Cek apakah Windows dengan pesan error jelas"""
        if not self.is_windows:
            self.last_error = "Notifikasi hanya tersedia di Windows"
            print(f"⚠️  {self.last_error}")
            return False
        return True
    
    def _escape_powershell(self, text):
        """Escape string untuk PowerShell"""
        if not text:
            return ""
        # Escape double quotes
        return text.replace('"', '`"').replace("'", "''")
    
    def send(self, title, message, duration=5, app_name="JPX"):
        """
        Kirim notifikasi Windows
        Args:
            title: Judul notifikasi (max 50 chars)
            message: Isi pesan (max 100 chars)
            duration: Durasi tampil (detik)
            app_name: Nama aplikasi (untuk notifikasi)
        Returns:
            dict: {
                'success': True/False,
                'method': 'powershell'/'console'/'none',
                'error': pesan error (jika gagal)
            }
        """
        result = {
            'success': False,
            'method': None,
            'error': None
        }
        
        # Validasi input
        if not title:
            title = "JPX Notification"
        if not message:
            message = "Pesan kosong"
        
        # Truncate panjang
        if len(title) > 50:
            title = title[:47] + "..."
        if len(message) > 100:
            message = message[:97] + "..."
        
        self._debug(f"Sending: '{title}' - '{message}'")
        
        # Cek Windows
        if not self._check_windows():
            result['error'] = self.last_error
            return result
        
        # Method 1: PowerShell Toast Notification (Windows 10/11)
        try:
            self._debug("Mencoba PowerShell Toast...")
            
            # Escape untuk PowerShell
            title_esc = self._escape_powershell(title)
            msg_esc = self._escape_powershell(message)
            app_esc = self._escape_powershell(app_name)
            
            # Buat XML template untuk notifikasi
            xml_template = f'''<?xml version="1.0" encoding="utf-8"?>
<toast duration="short">
  <visual>
    <binding template="ToastText02">
      <text id="1">{title_esc}</text>
      <text id="2">{msg_esc}</text>
    </binding>
  </visual>
</toast>'''
            
            # Simpan XML ke file temporary (hindari masalah encoding)
            with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False, encoding='utf-8') as f:
                f.write(xml_template)
                xml_path = f.name
            
            self._debug(f"XML saved to {xml_path}")
            
            # PowerShell script yang lebih robust
            ps_script = f'''
$ErrorActionPreference = "Stop"
try {{
    # Load required assemblies
    [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
    [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null

    # Read XML from file
    $xmlContent = Get-Content -Path "{xml_path}" -Raw
    $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
    $xml.LoadXml($xmlContent)

    # Create and show toast
    $toast = New-Object Windows.UI.Notifications.ToastNotification $xml
    $notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("{app_esc}")
    $notifier.Show($toast)

    Write-Host "SUCCESS"
}}
catch {{
    Write-Host "ERROR: $_"
    exit 1
}}
'''
            # Jalankan PowerShell dengan timeout
            self._debug("Running PowerShell...")
            process = subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps_script],
                capture_output=True,
                text=True,
                timeout=duration + 2,  # Extra time
                encoding='utf-8',
                errors='ignore'
            )
            
            # Hapus file temporary
            try:
                os.unlink(xml_path)
            except:
                pass
            
            # Cek hasil
            self._debug(f"PowerShell output: {process.stdout}")
            self._debug(f"PowerShell error: {process.stderr}")
            
            if "SUCCESS" in process.stdout:
                result['success'] = True
                result['method'] = 'powershell'
                return result
            else:
                self.last_error = process.stderr or "PowerShell gagal"
                self._debug(f"PowerShell error: {self.last_error}")
        
        except subprocess.TimeoutExpired:
            self.last_error = "PowerShell timeout"
            self._debug("PowerShell timeout")
        except FileNotFoundError:
            self.last_error = "PowerShell tidak ditemukan"
            self._debug("PowerShell not found")
        except Exception as e:
            self.last_error = str(e)
            self._debug(f"PowerShell exception: {e}")
        
        # Method 2: Fallback ke console
        try:
            self._debug("Falling back to console notification")
            
            # Simple box di console
            box_width = 60
            print("\n" + "╔" + "═" * box_width + "╗")
            print(f"║ {title:^{box_width-2}} ║")
            print("╠" + "═" * box_width + "╣")
            
            # Split message jadi beberapa baris
            words = message.split()
            lines = []
            current_line = ""
            
            for word in words:
                if len(current_line) + len(word) + 1 <= box_width - 4:
                    if current_line:
                        current_line += " " + word
                    else:
                        current_line = word
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
            
            if current_line:
                lines.append(current_line)
            
            for line in lines:
                print(f"║ {line:<{box_width-2}} ║")
            
            print("╚" + "═" * box_width + "╝")
            
            result['success'] = True
            result['method'] = 'console'
            return result
            
        except Exception as e:
            self.last_error = f"Console fallback error: {e}"
            self._debug(self.last_error)
        
        # Method 3: Simple print
        try:
            print(f"\n[{title}] {message}")
            result['success'] = True
            result['method'] = 'print'
            return result
        except:
            pass
        
        # Semua gagal
        result['error'] = self.last_error or "Unknown error"
        return result
    
    # ========== SHORTCUTS ==========
    def info(self, message, title="Info"):
        """Notifikasi info"""
        return self.send(title, message)
    
    def success(self, message, title="Sukses ✓"):
        """Notifikasi sukses"""
        return self.send(title, message)
    
    def warning(self, message, title="Peringatan ⚠"):
        """Notifikasi warning"""
        return self.send(title, message)
    
    def error(self, message, title="Error ✗"):
        """Notifikasi error"""
        return self.send(title, message)
    
    # ========== UTILITY ==========
    def test(self):
        """Test semua method notifikasi"""
        print("🧪 Testing notification module...")
        
        results = []
        results.append(self.info("Ini pesan info"))
        results.append(self.success("Ini pesan sukses"))
        results.append(self.warning("Ini pesan peringatan"))
        results.append(self.error("Ini pesan error"))
        
        # Summary
        print("\n" + "="*50)
        print("TEST RESULTS:")
        for i, res in enumerate(results):
            status = "✅" if res['success'] else "❌"
            print(f"{status} Method {i+1}: {res.get('method', 'failed')}")
        print("="*50)
        
        return results
    
    def get_last_error(self):
        """Ambil error terakhir"""
        return self.last_error
    
    def enable_debug(self):
        """Aktifkan mode debug"""
        self.debug_mode = True
        return True
    
    def disable_debug(self):
        """Nonaktifkan mode debug"""
        self.debug_mode = False
        return True

# Ekspor instance notification
exports = {
    'notification': Notification()
}