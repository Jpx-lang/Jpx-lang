# library/scanner.py
import os

class Scanner:
    def text(self, prompt, default=None, required=False):
        """Input teks dengan default value dan required flag"""
        while True:
            if default is not None:
                print(prompt + " [" + str(default) + "]: ", end="")
            else:
                print(prompt, end="")
            
            val = input().strip()
            
            if val == "" and default is not None:
                return default
            
            if required and val == "":
                print("❌ Field ini wajib diisi!")
                continue
            
            return val
    
    def number(self, prompt, default=None, min_val=None, max_val=None):
        """Input angka dengan range"""
        while True:
            if default is not None:
                print(prompt + " [" + str(default) + "]: ", end="")
            else:
                print(prompt, end="")
            
            try:
                val = int(input().strip())
            except:
                if default is not None:
                    return default
                print("❌ Input angka!")
                continue
            
            if min_val is not None and val < min_val:
                print("❌ Minimal " + str(min_val) + "!")
                continue
            if max_val is not None and val > max_val:
                print("❌ Maksimal " + str(max_val) + "!")
                continue
            
            return val
    
    def yesno(self, prompt, default=True):
        """Input ya/tidak"""
        while True:
            default_str = " (Y/n)" if default else " (y/N)"
            print(prompt + default_str + ": ", end="")
            
            val = input().strip().lower()
            
            if val == "":
                return default
            if val in ['y', 'yes', 'ya']:
                return True
            if val in ['n', 'no', 'tidak']:
                return False
            
            print("❌ Jawab y/n")
    
    def pause(self):
        """Pause sampai user tekan enter"""
        input("Tekan Enter...")
        return True

exports = {'scanner': Scanner()}