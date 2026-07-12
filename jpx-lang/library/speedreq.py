import urllib.request
import urllib.parse
import json
import ssl
import threading
import time
import os
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor, as_completed

# Abaikan SSL untuk kecepatan
ssl._create_default_https_context = ssl._create_unverified_context

# ========== CACHE SYSTEM ==========
class LRUCache:
    """Least Recently Used Cache untuk response"""
    def __init__(self, capacity=100):
        self.cache = OrderedDict()
        self.capacity = capacity
    
    def get(self, key):
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key, value):
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
    
    def clear(self):
        self.cache.clear()

# ========== CONNECTION POOL ==========
class ConnectionPool:
    """Pool koneksi untuk reuse connection"""
    def __init__(self, max_connections=10):
        self.max_connections = max_connections
        self.connections = []
        self.lock = threading.Lock()
    
    def get_connection(self):
        with self.lock:
            if self.connections:
                return self.connections.pop()
            return None
    
    def return_connection(self, conn):
        with self.lock:
            if len(self.connections) < self.max_connections:
                self.connections.append(conn)

# ========== SUPER FAST RESPONSE ==========
class SuperResponse:
    """Response object super cepat"""
    __slots__ = ('status', 'body', 'headers', 'url', '_json', 'elapsed')
    
    def __init__(self, status, body, headers, url, elapsed=0):
        self.status = status
        self.body = body
        self.headers = headers
        self.url = url
        self._json = None
        self.elapsed = elapsed
    
    @property
    def json(self):
        """Parse JSON super cepat (dengan cache)"""
        if self._json is None:
            try:
                self._json = json.loads(self.body)
            except:
                self._json = {}
        return self._json
    
    @property
    def ok(self):
        return 200 <= self.status < 300
    
    @property
    def text(self):
        return self.body
    
    def __str__(self):
        return f"<SuperResponse [{self.status}] in {self.elapsed:.3f}s>"

# ========== SUPER FAST REQUESTS ENGINE ==========
class SuperRequests:
    """Super Fast HTTP Requests Engine"""
    
    def __init__(self):
        self.user_agent = "JPX-Speed/2.0 (Super Fast)"
        self.timeout = 10
        self.max_workers = 20
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)
        self.cache = LRUCache(capacity=200)
        self.pool = ConnectionPool(max_connections=50)
        self.stats = {
            'total_requests': 0,
            'cache_hits': 0,
            'total_time': 0
        }
    
    def _request(self, method, url, data=None, headers=None, timeout=None, use_cache=True):
        """Internal request dengan kecepatan maksimal"""
        
        start_time = time.time()
        self.stats['total_requests'] += 1
        
        # Buat cache key
        cache_key = f"{method}:{url}:{str(data)}"
        
        # Cek cache
        if use_cache and method == 'GET':
            cached = self.cache.get(cache_key)
            if cached:
                self.stats['cache_hits'] += 1
                return cached
        
        try:
            # Optimasi DNS
            import socket
            old_timeout = socket.getdefaulttimeout()
            socket.setdefaulttimeout(timeout or self.timeout)
            
            # Buat request dengan optimasi
            req = urllib.request.Request(
                url, 
                method=method,
                headers={
                    'User-Agent': self.user_agent,
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive'
                }
            )
            
            # Tambah headers custom
            if headers:
                for k, v in headers.items():
                    req.add_header(k, v)
            
            # Handle data
            if data:
                if isinstance(data, dict):
                    data = json.dumps(data).encode('utf-8')
                    req.add_header('Content-Type', 'application/json')
                elif isinstance(data, str):
                    data = data.encode('utf-8')
            
            # Kirim request dengan timeout
            timeout_val = timeout or self.timeout
            with urllib.request.urlopen(req, data=data, timeout=timeout_val) as resp:
                status = resp.status
                body = resp.read().decode('utf-8', errors='ignore')
                headers = dict(resp.getheaders())
                
                elapsed = time.time() - start_time
                self.stats['total_time'] += elapsed
                
                response = SuperResponse(status, body, headers, url, elapsed)
                
                # Simpan ke cache
                if use_cache and method == 'GET' and status == 200:
                    self.cache.put(cache_key, response)
                
                return response
                
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8', errors='ignore') if hasattr(e, 'read') else str(e)
            return SuperResponse(e.code, body, dict(e.headers), url, time.time() - start_time)
        except Exception as e:
            return SuperResponse(0, str(e), {}, url, time.time() - start_time)
        finally:
            socket.setdefaulttimeout(old_timeout)
    
    # ========== METHODS SUPER CEPAT ==========
    
    def fetch(self, url, headers=None, timeout=None):
        """GET request super cepat"""
        return self._request('GET', url, headers=headers, timeout=timeout)
    
    def get(self, url, headers=None, timeout=None):
        """Alias untuk fetch"""
        return self.fetch(url, headers, timeout)
    
    def grab(self, url, headers=None, timeout=None):
        """Alias untuk fetch"""
        return self.fetch(url, headers, timeout)
    
    def send(self, url, data=None, headers=None, timeout=None):
        """POST request super cepat"""
        return self._request('POST', url, data=data, headers=headers, timeout=timeout, use_cache=False)
    
    def post(self, url, data=None, headers=None, timeout=None):
        """Alias untuk send"""
        return self.send(url, data, headers, timeout)
    
    def put(self, url, data=None, headers=None, timeout=None):
        """PUT request"""
        return self._request('PUT', url, data=data, headers=headers, timeout=timeout, use_cache=False)
    
    def delete(self, url, headers=None, timeout=None):
        """DELETE request"""
        return self._request('DELETE', url, headers=headers, timeout=timeout, use_cache=False)
    
    # ========== PARALLEL REQUESTS ==========
    
    def fetch_many(self, urls, headers=None, timeout=None):
        """GET multiple URLs secara paralel - SUPER CEPAT!"""
        results = []
        futures = []
        
        for url in urls:
            future = self.executor.submit(self.fetch, url, headers, timeout)
            futures.append((url, future))
        
        for url, future in futures:
            try:
                result = future.result(timeout=timeout or self.timeout)
                results.append(result)
            except Exception as e:
                results.append(SuperResponse(0, str(e), {}, url, 0))
        
        return results
    
    def fetch_batch(self, urls, batch_size=10, headers=None, timeout=None):
        """GET URLs dalam batch - untuk menghindari overload"""
        results = []
        for i in range(0, len(urls), batch_size):
            batch = urls[i:i+batch_size]
            batch_results = self.fetch_many(batch, headers, timeout)
            results.extend(batch_results)
        return results
    
    # ========== STREAMING ==========
    
    def stream(self, url, chunk_size=8192, headers=None):
        """Stream data untuk file besar"""
        try:
            req = urllib.request.Request(url, headers={'User-Agent': self.user_agent})
            if headers:
                for k, v in headers.items():
                    req.add_header(k, v)
            
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                while True:
                    chunk = resp.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk
        except Exception as e:
            yield f"Error: {e}".encode()
    
    # ========== DOWNLOAD ==========
    
    def download(self, url, save_path, headers=None, progress=True):
        """Download file dengan progress bar"""
        try:
            req = urllib.request.Request(url, headers={'User-Agent': self.user_agent})
            if headers:
                for k, v in headers.items():
                    req.add_header(k, v)
            
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                total_size = int(resp.headers.get('Content-Length', 0))
                downloaded = 0
                
                with open(save_path, 'wb') as f:
                    while True:
                        chunk = resp.read(8192)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if progress and total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"\rDownload: {percent:.1f}% ({downloaded}/{total_size} bytes)", end='')
                
                if progress:
                    print()
                return f"Download selesai: {save_path}"
        except Exception as e:
            return f"Download gagal: {e}"
    
    # ========== CACHE MANAGEMENT ==========
    
    def clear_cache(self):
        """Bersihkan cache"""
        self.cache.clear()
        return "Cache cleared"
    
    def cache_info(self):
        """Info cache"""
        return {
            'size': len(self.cache.cache),
            'capacity': self.cache.capacity,
            'hits': self.stats['cache_hits'],
            'total_requests': self.stats['total_requests']
        }
    
    # ========== STATS ==========
    
    def get_stats(self):
        """Statistik performa"""
        avg_time = 0
        if self.stats['total_requests'] > 0:
            avg_time = self.stats['total_time'] / self.stats['total_requests']
        
        return {
            'total_requests': self.stats['total_requests'],
            'cache_hits': self.stats['cache_hits'],
            'cache_hit_rate': f"{(self.stats['cache_hits']/max(1,self.stats['total_requests'])*100):.1f}%",
            'avg_response_time': f"{avg_time:.3f}s",
            'total_time': f"{self.stats['total_time']:.2f}s"
        }
    
    def reset_stats(self):
        """Reset statistik"""
        self.stats = {'total_requests': 0, 'cache_hits': 0, 'total_time': 0}
        return "Stats reset"
    
    # ========== BATCH OPERATIONS ==========
    
    def multi_request(self, requests_list):
        """Multiple requests berbeda dalam sekali jalan"""
        results = []
        futures = []
        
        for req in requests_list:
            method = req.get('method', 'GET')
            url = req.get('url')
            data = req.get('data')
            headers = req.get('headers')
            
            if method.upper() == 'GET':
                future = self.executor.submit(self.fetch, url, headers)
            elif method.upper() == 'POST':
                future = self.executor.submit(self.send, url, data, headers)
            else:
                future = self.executor.submit(self._request, method.upper(), url, data, headers)
            
            futures.append(future)
        
        for future in futures:
            try:
                results.append(future.result())
            except:
                results.append(None)
        
        return results

# ========== EXPORTS ==========
exports = {
    'speedreq': SuperRequests()
}