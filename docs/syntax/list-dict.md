# List dan Dict

## List

List ditulis dengan kurung siku, elemen dipisah koma, index mulai dari 0:

```jpx
global [l = [10, 20, 30]];

print l;                 # [10, 20, 30]
print l[0];              # 10
print len(l);            # 3
```

Elemen bisa berupa tipe campuran: `[1, "dua", true, [3]]`.

### Method `push`

`push` menambahkan elemen di akhir list **langsung pada list aslinya**:

```jpx
global [l = [3, 1, 2]];

l.push(4);
print l;                 # [3, 1, 2, 4]
```

### Index di Interpolasi

Akses elemen di dalam `${...}` juga bisa:

```jpx
global [nums = [3, 1, 4]];
print "elemen pertama: ${nums[0]}";     # elemen pertama: 3
```

### Modul `array`

Operasi list yang lebih kaya ada di modul bawaan `[array]`:

```jpx
[array];

global [nums = [3, 1, 4, 1, 5]];

print array.sum(nums);       # 14
print array.max(nums);       # 5
print array.min(nums);       # 1
print array.first(nums);     # 3
print array.last(nums);      # 5
print array.sort(nums);      # [1, 1, 3, 4, 5]
print array.reverse(nums);   # [5, 1, 4, 1, 3]
print array.contains(nums, 4);   # True
print array.join(nums, "-");     # 3-1-4-1-5
```

Fungsi `array` yang tersedia:
`push` `pop` `first` `last` `contains` `indexOf` `count` `reverse` `sort` `sum` `max`
`min` `join` `slice`

## Dict

Dict ditulis dengan kurung kurawal, pasangan `"key": nilai`:

```jpx
global [d = {"nama": "JPX", "ver": "A2"}];

print d["nama"];         # JPX
print "ver" in d;        # True
```

- Akses key memakai kurung siku: `d["nama"]`.
- Uji keberadaan key memakai operator `in`.
- Saat dicetak, dict tampil bergaya repr Python: `{'nama': 'JPX', 'ver': 'A2'}`
  (kutip tunggal).

### Menulis Ulang Nilai Dict

```jpx
global [d = {"hitung": 1}];
d["hitung"] = d["hitung"] + 1;
print d["hitung"];          # 2
```

## Iterasi

`for ... in` mengiterasi list; untuk dict, iterasi dilakukan atas list key-nya:

```jpx
global [d = {"a": 1, "b": 2}];
for k in ["a", "b"] {
    print k + " = " + str(d[k]);
}
```

## Halaman Terkait

- [modul.md](modul.md) — cara mengimpor `[array]` dan modul lain
- [string.md](string.md) — `split()` dan `toCharArray()` menghasilkan list
- [kontrol-alur.md](kontrol-alur.md) — `for ... in` dan `break`/`continue`
