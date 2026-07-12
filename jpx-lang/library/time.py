import time as _time
import datetime as _datetime

class TimeModule:
    @property
    def now(self):
        """Mengembalikan waktu sekarang dalam format YYYY-MM-DD HH:MM:SS"""
        return _datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @property
    def today(self):
        """Mengembalikan tanggal hari ini dalam format YYYY-MM-DD"""
        return _datetime.date.today().strftime("%Y-%m-%d")
    
    @property
    def year(self):
        """Mengembalikan tahun sekarang"""
        return _datetime.datetime.now().year
    
    @property
    def month(self):
        """Mengembalikan bulan sekarang (1-12)"""
        return _datetime.datetime.now().month
    
    @property
    def day(self):
        """Mengembalikan tanggal hari ini (1-31)"""
        return _datetime.datetime.now().day
    
    @property
    def hour(self):
        """Mengembalikan jam sekarang (0-23)"""
        return _datetime.datetime.now().hour
    
    @property
    def minute(self):
        """Mengembalikan menit sekarang (0-59)"""
        return _datetime.datetime.now().minute
    
    @property
    def second(self):
        """Mengembalikan detik sekarang (0-59)"""
        return _datetime.datetime.now().second
    
    @property
    def timestamp(self):
        """Mengembalikan Unix timestamp (detik sejak 1970-01-01)"""
        return _time.time()
    
    def wait(self, detik):
        """Menunggu selama detik tertentu"""
        _time.sleep(detik)
        return True
    
    def sleep(self, detik):
        """Alias untuk wait"""
        _time.sleep(detik)
        return True
    
    def format(self, format_str="%Y-%m-%d %H:%M:%S"):
        """Mengembalikan waktu dengan format kustom"""
        return _datetime.datetime.now().strftime(format_str)
    
    def parse(self, date_string, format_str="%Y-%m-%d"):
        """Parse string menjadi timestamp (dalam detik)"""
        try:
            dt = _datetime.datetime.strptime(date_string, format_str)
            return dt.timestamp()
        except:
            return 0
    
    def diff(self, waktu1, waktu2, unit="detik"):
        """Menghitung selisih dua waktu dalam unit tertentu"""
        try:
            if isinstance(waktu1, (int, float)) and isinstance(waktu2, (int, float)):
                selisih = abs(waktu1 - waktu2)
            else:
                fmt = "%Y-%m-%d %H:%M:%S"
                dt1 = _datetime.datetime.strptime(str(waktu1), fmt)
                dt2 = _datetime.datetime.strptime(str(waktu2), fmt)
                selisih = abs((dt1 - dt2).total_seconds())
            
            if unit in ["detik", "second"]:
                return selisih
            elif unit in ["menit", "minute"]:
                return selisih / 60
            elif unit in ["jam", "hour"]:
                return selisih / 3600
            elif unit in ["hari", "day"]:
                return selisih / 86400
            else:
                return selisih
        except:
            return 0
    
    def timer(self, detik, callback=None):
        """Timer dengan callback setelah detik tertentu"""
        _time.sleep(detik)
        if callback:
            return callback()
        return True
    
    def stopwatch(self):
        """Mengembalikan object stopwatch"""
        class Stopwatch:
            def __init__(self):
                self.start_time = None
                self.end_time = None
            
            def start(self):
                self.start_time = _time.time()
                return self
            
            def stop(self):
                self.end_time = _time.time()
                return self
            
            def elapsed(self):
                if self.end_time:
                    return self.end_time - self.start_time
                return _time.time() - self.start_time
            
            def reset(self):
                self.start_time = _time.time()
                self.end_time = None
                return self
        
        return Stopwatch()

exports = {
    'time': TimeModule()
}