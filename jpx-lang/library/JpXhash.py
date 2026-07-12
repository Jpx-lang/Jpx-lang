"""
Modul JpXhash untuk JPX
Encoding dan decoding custom untuk huruf A-Z
"""

class JpXhash:
    def __init__(self):
        # Aturan mapping untuk huruf A-Z
        self.encode_map = {
            'A': '^$HBIE247842BC9U',
            'B': '4&^UVB47FCB92UV',
            'C': '9*KJH78DFG32HJ5',
            'D': '2@MNB65RTY89UI7',
            'E': '7#QWE12ASD45DF6',
            'F': '5$RFV89TGB23YH8',
            'G': '1%UJM56KIO12KL9',
            'H': '8^YHN34BGT78OP0',
            'I': '3&EDC90PLK56HY4',
            'J': '6*IKM78NBV21ED3',
            'K': '4@QAZ12WSX34CDE',
            'L': '9#RFV56YHN78UJM',
            'M': '2$TGB89PLK01QAZ',
            'N': '7%UJM23EDC45RFV',
            'O': '1^YHN67BGT89TGB',
            'P': '5&EDC90IKM12PLK',
            'Q': '3*RFV34QAZ56WSX',
            'R': '8@TGB78UJM90EDC',
            'S': '4#YHN12PLK23RFV',
            'T': '9$EDC45QAZ67TGB',
            'U': '2%RFV78UJM89YHN',
            'V': '7^TGB90PLK01IKM',
            'W': '1&UJM23EDC45RFV',
            'X': '5*YHN56TGB78UJM',
            'Y': '3@PLK89QAZ12WSX',
            'Z': '8#RFV34EDC56TGB'
        }
        
        # Buat reverse mapping untuk decode
        self.decode_map = {}
        for key, value in self.encode_map.items():
            self.decode_map[value] = key
        
        # Aturan tambahan untuk angka dan simbol
        self.encode_map.update({
            '0': '!@#ZERO123!@#',
            '1': '$%^ONE456$%^',
            '2': '&*TWO789&*',
            '3': '()THREE012()',
            '4': '-+FOUR345-+',
            '5': '[]FIVE678[]',
            '6': '{}SIX901{}',
            '7': ';:SEVEN234;:',
            '8': '",EIGHT567",',
            '9': '<>NINE890<>',
            ' ': '___SPACE___',
            '.': '...DOT...',
            ',': ',,,COMMA,,,',
            '!': '!!!EXCL!!!',
            '?': '???QUES???',
            '@': '@@@AT@@@',
            '#': '###HASH###',
            '$': '$$$DOL$$$',
            '%': '%%%PER%%%',
            '^': '^^^CAR^^^',
            '&': '&&&AMP&&&',
            '*': '***STR***',
            '(': '((LPR(((',
            ')': ')))RPR)))',
            '-': '---DASH---',
            '_': '___UND___',
            '+': '+++PLS+++',
            '=': '===EQL===',
            '[': '[[LBR[[',
            ']': ']]RBR]]',
            '{': '{{LBR{{',
            '}': '}}RBR}}',
            '|': '|||PIP|||',
            '\\': '\\\\BSL\\\\',
            '/': '///FSL///',
            ':': ':::COL:::',
            ';': ';;;SCL;;;',
            '"': '"""QUO"""',
            "'": "'''APO'''"
        })
        
        # Update decode map dengan aturan tambahan
        for key, value in self.encode_map.items():
            self.decode_map[value] = key
    
    def encode(self, text):
        """
        Encode string menggunakan aturan JpXhash
        Contoh: JpXhash.encode("HELLO") -> hasil encode
        """
        try:
            if not isinstance(text, str):
                text = str(text)
            
            result = []
            for char in text.upper():  # Konversi ke uppercase untuk konsistensi
                if char in self.encode_map:
                    result.append(self.encode_map[char])
                else:
                    # Jika karakter tidak ada di mapping, biarkan apa adanya
                    result.append(char)
            
            return ''.join(result)
        except Exception as e:
            return f"<error: {e}>"
    
    def decode(self, encoded_text):
        """
        Decode string menggunakan aturan JpXhash
        Contoh: JpXhash.decode(encoded) -> teks asli
        """
        try:
            if not isinstance(encoded_text, str):
                encoded_text = str(encoded_text)
            
            result = []
            i = 0
            length = len(encoded_text)
            
            while i < length:
                found = False
                # Cari pattern terpanjang yang cocok (untuk efisiensi)
                for pattern in sorted(self.decode_map.keys(), key=len, reverse=True):
                    if encoded_text.startswith(pattern, i):
                        result.append(self.decode_map[pattern])
                        i += len(pattern)
                        found = True
                        break
                
                if not found:
                    # Jika tidak ada pattern yang cocok, ambil karakter biasa
                    result.append(encoded_text[i])
                    i += 1
            
            return ''.join(result)
        except Exception as e:
            return f"<error: {e}>"
    
    def encode_letter(self, letter):
        """
        Encode satu huruf
        Contoh: JpXhash.encode_letter("A") -> "^$HBIE247842BC9U"
        """
        letter = letter.upper()
        if letter in self.encode_map:
            return self.encode_map[letter]
        return letter
    
    def decode_letter(self, encoded):
        """
        Decode satu huruf
        Contoh: JpXhash.decode_letter("^$HBIE247842BC9U") -> "A"
        """
        if encoded in self.decode_map:
            return self.decode_map[encoded]
        return encoded
    
    def get_mapping(self):
        """
        Mengembalikan seluruh mapping yang digunakan
        """
        return self.encode_map
    
    def add_mapping(self, char, pattern):
        """
        Menambahkan mapping baru
        """
        char = char.upper()
        self.encode_map[char] = pattern
        self.decode_map[pattern] = char
        return True
    
    def remove_mapping(self, char):
        """
        Menghapus mapping untuk karakter tertentu
        """
        char = char.upper()
        if char in self.encode_map:
            pattern = self.encode_map[char]
            del self.encode_map[char]
            del self.decode_map[pattern]
            return True
        return False
    
    def is_encoded(self, text):
        """
        Cek apakah text kemungkinan sudah diencode
        (mengandung pattern yang ada di decode_map)
        """
        for pattern in self.decode_map.keys():
            if pattern in text:
                return True
        return False
    
    def encode_file(self, input_file, output_file=None):
        """
        Encode isi file
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            encoded = self.encode(content)
            
            if output_file is None:
                output_file = input_file + '.jpxhash'
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(encoded)
            
            return {
                'success': True,
                'input': input_file,
                'output': output_file,
                'size': len(encoded)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def decode_file(self, input_file, output_file=None):
        """
        Decode isi file
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            decoded = self.decode(content)
            
            if output_file is None:
                if input_file.endswith('.jpxhash'):
                    output_file = input_file[:-8]  # hapus .jpxhash
                else:
                    output_file = input_file + '.decoded'
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(decoded)
            
            return {
                'success': True,
                'input': input_file,
                'output': output_file,
                'size': len(decoded)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def visualize(self, text):
        """
        Menampilkan visualisasi encoding per karakter
        """
        try:
            result = []
            for char in str(text).upper():
                if char in self.encode_map:
                    result.append({
                        'char': char,
                        'encoded': self.encode_map[char],
                        'length': len(self.encode_map[char])
                    })
                else:
                    result.append({
                        'char': char,
                        'encoded': char,
                        'length': 1
                    })
            return result
        except:
            return []

# Ekspor instance JpXhash
exports = {
    'JpXhash': JpXhash()
}