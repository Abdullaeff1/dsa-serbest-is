# Müasir Data Strukturları və Alqoritmlər — Sərbəst İş (Mövzu 1–5)

3 nəfərlik komanda layihəsi. Məqsəd: əsas data strukturlarını **özümüz implementasiya etmək**, sadə mini-tətbiqlər göstərmək və **eksperimental performans** müqayisəsi aparmaq.

## Komanda

- Səid Abdullayev — Array / Dynamic Array, Hash Table
- Nicat İbrahimov — Linked List, Stack / Queue / Deque, mini-tətbiqlər
- Yunus Həşimov — BST, benchmark, sənədləşdirmə

Ətraflı rol bölgüsü: [CONTRIBUTORS.md](CONTRIBUTORS.md)

## Nə implementasiya olunub?

| # | Mövzu | Fayllar |
|---|---|---|
| 1 | Array və Dynamic Array performans analizi | `structures/array_ops.py` |
| 2 | Singly və Doubly Linked List müqayisəsi | `structures/linked_lists.py` |
| 3 | Stack, Queue, Deque + mini-tətbiq | `structures/sqd.py`, `apps/` |
| 4 | Chaining Hash Table | `structures/hash_table.py` |
| 5 | BST + balans problemi analizi | `structures/bst.py` |

### Mini-tətbiqlər (mövzu 3)

- **Bracket Checker** — Stack ilə mötərizə tarazlığı
- **Ticket Line** — Queue ilə növbə (FIFO)
- **Music Playlist** — Deque ilə ön/son əlavə

## Layihə strukturu

```text
dsa-serbest-is/
├── structures/       # data strukturları
├── apps/             # mini-tətbiqlər
├── benchmarks/       # performans ölçmələri
├── tests/            # sadə testlər
├── docs/             # hesabat və təqdimat konturu
├── results/          # benchmark çıxışları
├── main.py           # konsol menyusu
└── README.md
```

## Tələblər

- Python 3.10+ (xarici paket lazım deyil)

## İşə salma

```bash
cd dsa-serbest-is
python main.py
```

Testlər:

```bash
python tests/test_all.py
```

Benchmark:

```bash
python benchmarks/run_benchmarks.py
```

Nəticələr `results/benchmark_results.txt` faylına yazılır.

## Mürəkkəblik (qısa)

| Struktur | Axtarış | Əlavə | Silmə |
|---|---|---|---|
| Fixed Array | O(n) | sonda O(1)* | O(n) |
| Dynamic Array | O(n) | sonda amortized O(1) | O(n) |
| Singly Linked List | O(n) | başda O(1), sonda O(n) | başda O(1) |
| Doubly Linked List | O(n) | hər iki ucda O(1) | hər iki ucda O(1) |
| Stack / Queue / Deque | — | O(1)** | O(1)** |
| Hash Table (chaining) | ortalama O(1) | ortalama O(1) | ortalama O(1) |
| BST | ortalama O(log n), worst O(n) | eyni | eyni |

\* Fixed Array dolu olanda əlavə mümkün deyil.  
\*\* Bizim implementasiyada Stack Dynamic Array üzərindədir (amortized O(1)).

## Sənədlər

- Texniki hesabat: [docs/hesabat.md](docs/hesabat.md)
- Təqdimat konturu: [docs/teqdimat_outline.md](docs/teqdimat_outline.md)

## İstinadlar

1. Goodrich, Tamassia, Goldwasser — *Data Structures and Algorithms in Python*
2. Cormen et al. — *Introduction to Algorithms* (BST, hashing bölmələri)
3. Kurs sillabusu: *Müasir Data Strukturları və Alqoritmlər* (sərbəst iş mövzuları 1–5)

> Qeyd: Digər qrupların repo strukturu yalnız ümumi yanaşma üçün nəzərdən keçirilib; kod və mini-tətbiqlər bu komandaya məxsusdur.
