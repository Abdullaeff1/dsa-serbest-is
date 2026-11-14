# Texniki hesabat — Sərbəst iş (Mövzu 1–5)

**Fənn:** Müasir Data Strukturları və Alqoritmlər  
**Komanda:** Səid Abdullayev, Nicat İbrahimov, Yunus Həşimov  
**Format:** Git repository + konsol tətbiqi + test/benchmark

---

## 1. Problem və məqsəd

Kursun ilk 5 sərbəst iş mövzusu üzrə əsas data strukturlarını hazır kitabxana sinifləri ilə deyil, **öz implementasiyamız** ilə öyrənmək lazımdır. Eyni zamanda:

- əməliyyatların **zaman/yaddaş mürəkkəbliyini** izah etmək,
- kiçik **test ssenariləri** yazmaq,
- **benchmark** ilə praktiki fərqləri göstərmək,
- Stack/Queue/Deque üçün **mini-tətbiq** nümayiş etdirmək tələb olunur.

## 2. Seçilmiş yanaşma

Dil olaraq **Python 3** seçilmişdir: sintaksis sadədir, kursun yeni başlayan səviyyəsinə uyğundur və xarici paket tələb etmir.

Hər struktur ayrı modulda saxlanılır (`structures/`). Mini-tətbiqlər `apps/` qovluğundadır. Ölçmələr `benchmarks/run_benchmarks.py` ilə aparılır.

### 2.1 Mövzu 1 — Array və Dynamic Array

- **FixedArray:** sabit tutum; dolanda `OverflowError`.
- **DynamicArray:** dolanda tutum **2 dəfə artırılır** (doubling); ölçü tutumun 1/4-nə düşəndə kiçildilir.

Eksperiment: `append`, ortada `insert`, `search` üçün n = 100, 1000, 5000.

### 2.2 Mövzu 2 — Singly və Doubly Linked List

- Singly: yalnız `next`; sonda əlavə/silmə O(n).
- Doubly: `prev`/`next` + `tail`; hər iki ucda O(1).

Müqayisənin əsas nəticəsi: iki istiqamətli siyahı uclar üzrə əməliyyatlarda daha əlverişlidir, amma hər düyün üçün əlavə yaddaş (`prev`) tələb edir.

### 2.3 Mövzu 3 — Stack, Queue, Deque mini-tətbiq

| Struktur | Tətbiq | Ideya |
|---|---|---|
| Stack | Bracket Checker | Açılan mötərizə push, bağlanan pop/yoxla |
| Queue | Ticket Line | Müştərilər FIFO növbədə |
| Deque | Music Playlist | Mahnını həm önə, həm sona əlavə |

### 2.4 Mövzu 4 — Hash Table (chaining)

Hər bucket Python siyahısıdır. Toqquşma olduqda eyni bucket-ə `(key, value)` əlavə olunur. Load factor ~0.75-i keçəndə tutum ikiqat artırılır və elementlər yenidən yerləşdirilir.

### 2.5 Mövzu 5 — BST və balans problemi

Klassik BST (özünü balanslaşdırmır). **Sıralı** insert ağacı demək olar ki, linked list-ə çevirir (height ≈ n−1). **Təsadüfi** insert isə adətən daha kiçik hündürlük verir. Bu, “balans problemi”nin sadə eksperimental sübutudur.

## 3. Mürəkkəblik analizi (Time / Space)

| Struktur | Search | Insert | Delete | Əlavə yaddaş |
|---|---|---|---|---|
| Fixed Array | O(n) | sonda O(1), ortada O(n) | O(n) | O(capacity) |
| Dynamic Array | O(n) | sonda amortized O(1) | O(n) | O(capacity) |
| Singly LL | O(n) | baş O(1), son O(n) | baş O(1), son O(n) | O(n) düyün |
| Doubly LL | O(n) | hər uc O(1) | hər uc O(1) | O(n) + prev |
| Stack | — | amortized O(1) | amortized O(1) | massiv |
| Queue | — | O(1) | O(1) | doubly list |
| Deque | — | O(1) | O(1) | doubly list |
| Hash Table | avg O(1), worst O(n) | avg O(1) | avg O(1) | bucket-lər |
| BST | avg O(log n), worst O(n) | eyni | eyni | O(n) |

## 4. Test ssenariləri

`tests/test_all.py` aşağıdakıları yoxlayır:

- FixedArray dolma xətası, DynamicArray böyüməsi
- Linked list əlavə/silmə sırası
- Stack LIFO, Queue FIFO, Deque iki uc
- Hash update / remove / resize
- BST inorder, delete, sıralı insert-də yüksək height
- Mini-tətbiqlərin düzgün davranışı

İşə salma: `python tests/test_all.py`

## 5. Benchmark və nəticələrin təhlili

Ölçmə aləti: `time.perf_counter_ns()`. Ölçülər maşından asılıdır; nisbi müqayisə vacibdir.

Gözlənilən müşahidələr:

1. **DynamicArray append** FixedArray-ə yaxın sürətdə qalır (amortized O(1)), amma FixedArray dolanda dayananır.
2. **Singly insert_back** Doubly insert_back-dən yavaşdır (O(n) vs O(1)).
3. **HashTable get** böyük n-də linear list axtarışından daha sabit qalır.
4. **BST sorted height** ≈ n−1; **random height** əhəmiyyətli dərəcədə kiçik olur — axtarış da buna görə fərqlənir.

Nəticə faylı: `results/benchmark_results.txt` (proqram işə salındlıqdan sonra yenilənir).

## 6. Trade-off-lar

- **Array** indeksə görə sürətlidir, amma ortada insert bahalıdır.
- **Linked list** uclarda rahatdır, amma təsadüfi indeks yoxdur.
- **Hash table** ortalama sürətlidir, amma worst-case və hash key tələbi var.
- **BST** sıralı məlumat üçün əlverişlidir, amma balans olmadan degenerasiya olur (AVL/Red-Black lazım ola bilər — bu kurs mərhələsində sadə BST kifayətdir).

## 7. Nəticə

Layihə mövzu 1–5 tələblərini ödəyir: implementasiya, mini-tətbiq, mürəkkəblik izahı, test və eksperimental müqayisə. Komanda işi modul bölgüsü və Git author tarixçəsi ilə sənədləşdirilib.

## 8. İstinadlar

1. Goodrich et al., *Data Structures and Algorithms in Python*
2. Cormen et al., *Introduction to Algorithms*
3. Kurs sillabusu — sərbəst iş mövzuları və qiymətləndirmə meyarları
