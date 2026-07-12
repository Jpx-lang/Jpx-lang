"""
notification.py - Modul notifikasi sederhana untuk Windows
"""

import os
import platform

# Cek platform
IS_WINDOWS = platform.system() == "Windows"

# Coba import library notifikasi
try:
    from plyer import notification as plyer_notification
    PLYER_AVAILABLE = True
except ImportError:
    PLYER_AVAILABLE = False

try:
    from win10toast import ToastNotifier
    WIN10TOAST_AVAILABLE = True
    toaster = ToastNotifier()
except ImportError:
    WIN10TOAST_AVAILABLE = False

class Notification:
    def __init__(self):
        pass
    
    def send(self, title, message, timeout=5):
        """
        Kirim notifikasi sederhana
        Args:
            title: Judul notifikasi
            message: Isi pesan
            timeout: Durasi tampil (detik)
        Returns:
            True jika berhasil, False jika gagal
        """
        if not IS_WINDOWS:
            print("Notifikasi hanya tersedia di Windows")
            return False
        
        # Coba dengan win10toast (rekomendasi)
        if WIN10TOAST_AVAILABLE:
            try:
                toaster.show_toast(
                    title,
                    message,
                    duration=timeout,
                    threaded=True
                )
                return True
            except:
                pass
        
        # Fallback ke plyer
        if PLYER_AVAILABLE:
            try:
                plyer_notification.notify(
                    title=title,
                    message=message,
                    timeout=timeout
                )
                return True
            except:
                pass
        
        print("Install win10toast: pip install win10toast")
        return False

# Ekspor instance notification
exports = {
    'notification': Notification()
}