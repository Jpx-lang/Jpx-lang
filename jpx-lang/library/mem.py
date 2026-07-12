# mem.py - JPX-X Memory Module
# Wrapper untuk mem.dll

import ctypes
import os
import sys

# Load DLL
dll_path = os.path.join(os.path.dirname(__file__), 'mem.dll')
if not os.path.exists(dll_path):
    dll_path = os.path.join(os.path.dirname(__file__), '..', 'c_modules', 'mem.dll')

try:
    mem_dll = ctypes.CDLL(dll_path)
    print(f"✅ mem.dll loaded from {dll_path}")
except Exception as e:
    print(f"❌ Failed to load mem.dll: {e}")
    print("Make sure mem.dll is in the same directory as mem.py")
    sys.exit(1)

# Define function signatures
mem_dll.mem_alloc.argtypes = [ctypes.c_int]
mem_dll.mem_alloc.restype = ctypes.c_void_p

mem_dll.mem_free.argtypes = [ctypes.c_void_p]
mem_dll.mem_free.restype = None

mem_dll.mem_read_byte.argtypes = [ctypes.c_void_p, ctypes.c_int]
mem_dll.mem_read_byte.restype = ctypes.c_ubyte

mem_dll.mem_write_byte.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_ubyte]
mem_dll.mem_write_byte.restype = None

mem_dll.mem_read_int.argtypes = [ctypes.c_void_p, ctypes.c_int]
mem_dll.mem_read_int.restype = ctypes.c_int

mem_dll.mem_write_int.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
mem_dll.mem_write_int.restype = None

mem_dll.mem_peek.argtypes = [ctypes.c_uint64]
mem_dll.mem_peek.restype = ctypes.c_ubyte

mem_dll.mem_poke.argtypes = [ctypes.c_uint64, ctypes.c_ubyte]
mem_dll.mem_poke.restype = None

mem_dll.mem_peek_int.argtypes = [ctypes.c_uint64]
mem_dll.mem_peek_int.restype = ctypes.c_int

mem_dll.mem_poke_int.argtypes = [ctypes.c_uint64, ctypes.c_int]
mem_dll.mem_poke_int.restype = None

# Windows-specific functions
if hasattr(mem_dll, 'mem_read_process'):
    mem_dll.mem_read_process.argtypes = [ctypes.c_int, ctypes.c_uint64, ctypes.c_void_p, ctypes.c_int]
    mem_dll.mem_read_process.restype = ctypes.c_int
    
    mem_dll.mem_write_process.argtypes = [ctypes.c_int, ctypes.c_uint64, ctypes.c_void_p, ctypes.c_int]
    mem_dll.mem_write_process.restype = ctypes.c_int


class Mem:
    """Low-level memory manipulation for JPX-X"""
    
    def __init__(self):
        self.warnings_shown = False
    
    def _warn(self):
        """Show warning only once"""
        if not self.warnings_shown:
            print("\n⚠️  WARNING: mem module can crash your computer!")
            print("   Use at your own risk. Always backup important data.\n")
            self.warnings_shown = True
    
    # ==================== ALLOCATION ====================
    
    def alloc(self, size):
        """Allocate memory block"""
        self._warn()
        return mem_dll.mem_alloc(size)
    
    def free(self, ptr):
        """Free allocated memory"""
        mem_dll.mem_free(ptr)
    
    # ==================== READ/WRITE ====================
    
    def read_byte(self, ptr, offset=0):
        """Read byte from memory"""
        return mem_dll.mem_read_byte(ptr, offset)
    
    def write_byte(self, ptr, offset, value):
        """Write byte to memory"""
        mem_dll.mem_write_byte(ptr, offset, value)
    
    def read_int(self, ptr, offset=0):
        """Read 4-byte integer"""
        return mem_dll.mem_read_int(ptr, offset)
    
    def write_int(self, ptr, offset, value):
        """Write 4-byte integer"""
        mem_dll.mem_write_int(ptr, offset, value)
    
    # ==================== DIRECT ACCESS ====================
    
    def peek(self, addr):
        """Read byte from absolute address"""
        self._warn()
        return mem_dll.mem_peek(addr)
    
    def poke(self, addr, value):
        """Write byte to absolute address"""
        self._warn()
        mem_dll.mem_poke(addr, value)
    
    def peek_int(self, addr):
        """Read int from absolute address"""
        self._warn()
        return mem_dll.mem_peek_int(addr)
    
    def poke_int(self, addr, value):
        """Write int to absolute address"""
        self._warn()
        mem_dll.mem_poke_int(addr, value)
    
    # ==================== PROCESS MEMORY (BYPASS) ====================
    
    def read_process(self, pid, addr, size):
        """Read from another process's memory"""
        if not hasattr(mem_dll, 'mem_read_process'):
            raise Exception("Process memory functions not available on this platform")
        
        self._warn()
        buffer = ctypes.create_string_buffer(size)
        result = mem_dll.mem_read_process(pid, addr, buffer, size)
        if result > 0:
            return buffer.raw[:result]
        return None
    
    def write_process(self, pid, addr, data):
        """Write to another process's memory"""
        if not hasattr(mem_dll, 'mem_write_process'):
            raise Exception("Process memory functions not available on this platform")
        
        self._warn()
        buffer = ctypes.create_string_buffer(data)
        return mem_dll.mem_write_process(pid, addr, buffer, len(data))
    
    # ==================== UTILITY ====================
    
    def get_module_base(self, module_name):
        """Get base address of loaded module"""
        return mem_dll.mem_get_module_base(module_name.encode())
    
    def scan(self, start, end, value):
        """Scan memory range for value"""
        results = []
        for addr in range(start, end, 4):
            try:
                if self.peek_int(addr) == value:
                    results.append(addr)
            except:
                pass
        return results
    
    # ==================== ALIASES ====================
    
    def read(self, ptr, offset=0):
        """Alias for read_byte"""
        return self.read_byte(ptr, offset)
    
    def write(self, ptr, offset, value):
        """Alias for write_byte"""
        self.write_byte(ptr, offset, value)


# Create instance
_mem = Mem()

# Export for JPX
exports = {
    'mem': _mem,
    'alloc': _mem.alloc,
    'free': _mem.free,
    'read': _mem.read,
    'write': _mem.write,
    'peek': _mem.peek,
    'poke': _mem.poke,
    'scan': _mem.scan,
}