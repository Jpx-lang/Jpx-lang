"""
Modul Requests untuk JPX
Mendukung HTTP/HTTPS requests dengan berbagai metode
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import ssl
import time
import os

class Response:
    """Objek response dari HTTP request"""
    def __init__(self, url, status_code, headers, body, elapsed_ms):
        self.url = url
        self.status_code = status_code
        self.headers = headers
        self.body = body
        self.elapsed_ms = elapsed_ms
        self.ok = 200 <= status_code < 300
        self.text = body
    
    def json(self):
        """Parse body sebagai JSON"""
        try:
            return json.loads(self.body)
        except:
            return None
    
    def __str__(self):
        return f"<Response [{self.status_code}]>"

class Requests:
    def __init__(self):
        self.default_headers = {
            'User-Agent': 'JPX-Requests/1.0',
            'Accept': '*/*'
        }
        self.timeout = 30
        self.verify_ssl = True
    
    def _current_time_ms(self):
        return int(time.time() * 1000)
    
    def fetch(self, url, options=None):
        """Fungsi utama untuk fetch URL"""
        if options is None:
            options = {}
        
        method = options.get('method', 'GET').upper()
        headers = options.get('headers', {})
        data = options.get('data', None)
        json_data = options.get('json', None)
        timeout = options.get('timeout', self.timeout)
        verify = options.get('verify', self.verify_ssl)
        
        # Merge headers
        req_headers = self.default_headers.copy()
        for key, value in headers.items():
            req_headers[key] = value
        
        # Prepare data
        post_data = None
        if json_data is not None:
            post_data = json.dumps(json_data).encode('utf-8')
            req_headers['Content-Type'] = 'application/json'
        elif data is not None:
            if isinstance(data, dict):
                post_data = urllib.parse.urlencode(data).encode('utf-8')
                req_headers['Content-Type'] = 'application/x-www-form-urlencoded'
            else:
                post_data = str(data).encode('utf-8')
        
        # Create request
        req = urllib.request.Request(url, data=post_data, headers=req_headers, method=method)
        
        # Handle SSL verify
        context = None
        if not verify:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
        
        start_time = self._current_time_ms()
        
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=context) as response:
                elapsed = self._current_time_ms() - start_time
                body = response.read().decode('utf-8', errors='ignore')
                headers = {}
                for key, value in response.getheaders():
                    headers[key] = value
                
                return Response(
                    url=url,
                    status_code=response.status,
                    headers=headers,
                    body=body,
                    elapsed_ms=elapsed
                )
                
        except urllib.error.HTTPError as e:
            elapsed = self._current_time_ms() - start_time
            body = e.read().decode('utf-8', errors='ignore') if hasattr(e, 'read') else str(e)
            headers = {}
            if hasattr(e, 'headers'):
                for key, value in e.headers.items():
                    headers[key] = value
            
            return Response(
                url=url,
                status_code=e.code,
                headers=headers,
                body=body,
                elapsed_ms=elapsed
            )
            
        except Exception as e:
            elapsed = self._current_time_ms() - start_time
            return Response(
                url=url,
                status_code=0,
                headers={},
                body=str(e),
                elapsed_ms=elapsed
            )
    
    # Method shortcuts
    def get(self, url, headers=None, timeout=None, verify=None):
        return self.fetch(url, {
            'method': 'GET',
            'headers': headers or {},
            'timeout': timeout or self.timeout,
            'verify': verify if verify is not None else self.verify_ssl
        })
    
    def post(self, url, data=None, json=None, headers=None, timeout=None, verify=None):
        return self.fetch(url, {
            'method': 'POST',
            'headers': headers or {},
            'data': data,
            'json': json,
            'timeout': timeout or self.timeout,
            'verify': verify if verify is not None else self.verify_ssl
        })
    
    def put(self, url, data=None, json=None, headers=None, timeout=None, verify=None):
        return self.fetch(url, {
            'method': 'PUT',
            'headers': headers or {},
            'data': data,
            'json': json,
            'timeout': timeout or self.timeout,
            'verify': verify if verify is not None else self.verify_ssl
        })
    
    def delete(self, url, headers=None, timeout=None, verify=None):
        return self.fetch(url, {
            'method': 'DELETE',
            'headers': headers or {},
            'timeout': timeout or self.timeout,
            'verify': verify if verify is not None else self.verify_ssl
        })
    
    def patch(self, url, data=None, json=None, headers=None, timeout=None, verify=None):
        return self.fetch(url, {
            'method': 'PATCH',
            'headers': headers or {},
            'data': data,
            'json': json,
            'timeout': timeout or self.timeout,
            'verify': verify if verify is not None else self.verify_ssl
        })
    
    def head(self, url, headers=None, timeout=None, verify=None):
        return self.fetch(url, {
            'method': 'HEAD',
            'headers': headers or {},
            'timeout': timeout or self.timeout,
            'verify': verify if verify is not None else self.verify_ssl
        })
    
    # URL utilities
    def urlparse(self, url):
        parsed = urllib.parse.urlparse(url)
        return {
            'scheme': parsed.scheme,
            'netloc': parsed.netloc,
            'path': parsed.path,
            'params': parsed.params,
            'query': parsed.query,
            'fragment': parsed.fragment,
            'hostname': parsed.hostname,
            'port': parsed.port,
            'username': parsed.username,
            'password': parsed.password
        }
    
    def urlencode(self, params):
        return urllib.parse.urlencode(params)
    
    def urldecode(self, query_string):
        parsed = urllib.parse.parse_qs(query_string)
        result = {}
        for key, value in parsed.items():
            result[key] = value[0] if len(value) == 1 else value
        return result
    
    # Download file (binary-safe streaming)
    def download(self, url, filename, headers=None, timeout=None, verify=None):
        """Download file dengan streaming chunk (binary-safe).

        Dulu implementasinya `res.body.encode('utf-8')` — body sudah
        terlebih dulu di-decode sebagai TEKS (errors='ignore'), sehingga
        file binary (exe, zip, tar) rusak permanen. Sekarang stream byte
        mentah ke disk per 64KB tanpa decode, plus:
          - tulis ke `<filename>.part` lalu os.replace() (atomic — tidak
            meninggalkan file setengah jadi bila download gagal)
          - return dict superset: success, filename, size, total,
            status_code, elapsed_ms
        Progress UI tidak perlu subprocess lagi: cukup poll fs.size(path)
        atau baca field total/size setelah selesai.
        """
        start_time = self._current_time_ms()
        req_headers = self.default_headers.copy()
        if headers:
            for key, value in headers.items():
                req_headers[key] = value

        context = None
        if verify is not None and not verify:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

        tmp_path = str(filename) + '.part'
        try:
            req = urllib.request.Request(url, headers=req_headers)
            with urllib.request.urlopen(req, timeout=timeout or self.timeout,
                                        context=context) as resp:
                total = 0
                try:
                    total = int(resp.headers.get('Content-Length') or 0)
                except (ValueError, TypeError):
                    total = 0
                written = 0
                with open(tmp_path, 'wb') as f:
                    while True:
                        chunk = resp.read(65536)
                        if not chunk:
                            break
                        f.write(chunk)
                        written += len(chunk)
                os.replace(tmp_path, str(filename))
                return {
                    'success': True,
                    'filename': str(filename),
                    'size': written,
                    'total': total,
                    'status_code': resp.status,
                    'elapsed_ms': self._current_time_ms() - start_time,
                }
        except urllib.error.HTTPError as e:
            self._cleanup_partial(tmp_path)
            return {
                'success': False,
                'error': f"HTTP {e.code}",
                'status_code': e.code,
            }
        except Exception as e:
            self._cleanup_partial(tmp_path)
            return {
                'success': False,
                'error': str(e),
                'status_code': 0,
            }

    def _cleanup_partial(self, tmp_path):
        """Hapus file .part sisa download gagal."""
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except OSError:
            pass
    
    # Settings
    def set_default_header(self, key, value):
        self.default_headers[key] = value
    
    def set_timeout(self, timeout):
        self.timeout = timeout
    
    def set_verify_ssl(self, verify):
        self.verify_ssl = verify

# Ekspor instance requests
exports = {
    'requests': Requests()
}
