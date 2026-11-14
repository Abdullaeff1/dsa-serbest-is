"""Generate presentation PPTX and technical report PDF (Azerbaijani)."""

from __future__ import annotations

import os
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

# Design tokens — academic teal / navy (not purple)
NAVY = RGBColor(0x0B, 0x2A, 0x3A)
TEAL = RGBColor(0x1A, 0x7A, 0x6D)
TEAL_LIGHT = RGBColor(0xE6, 0xF3, 0xF0)
SAND = RGBColor(0xF5, 0xF1, 0xEA)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
INK = RGBColor(0x1C, 0x24, 0x2B)
MUTED = RGBColor(0x5A, 0x66, 0x70)
ACCENT = RGBColor(0xC4, 0x5C, 0x26)  # terracotta only as small accent line


def _set_run(run, size=18, bold=False, color=INK, font="Calibri"):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = font


def _fill(shape, color):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()


def _blank_slide(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])  # blank


def _bg(slide, color=SAND):
    fill = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5)
    )
    _fill(fill, color)
    # send to back
    spTree = slide.shapes._spTree
    sp = fill._element
    spTree.remove(sp)
    spTree.insert(2, sp)
    return fill


def _sidebar(slide):
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.18), Inches(7.5)
    )
    _fill(bar, TEAL)
    return bar


def _top_band(slide, title):
    band = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15)
    )
    _fill(band, NAVY)
    accent = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.15), Inches(13.333), Inches(0.06)
    )
    _fill(accent, TEAL)

    box = slide.shapes.add_textbox(Inches(0.55), Inches(0.28), Inches(12.2), Inches(0.7))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = title
    _set_run(run, size=28, bold=True, color=WHITE, font="Calibri")
    return box


def _footer(slide, page, total):
    box = slide.shapes.add_textbox(Inches(0.55), Inches(7.05), Inches(10), Inches(0.35))
    p = box.text_frame.paragraphs[0]
    run = p.add_run()
    run.text = "DSA Sərbəst İş  ·  Mövzu 1–5  ·  Abdullaeff1/dsa-serbest-is"
    _set_run(run, size=11, color=MUTED)

    num = slide.shapes.add_textbox(Inches(11.6), Inches(7.05), Inches(1.3), Inches(0.35))
    p = num.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    run = p.add_run()
    run.text = f"{page} / {total}"
    _set_run(run, size=11, color=MUTED)


def _bullets(slide, lines, left=0.55, top=1.5, width=12.2, height=5.2, size=20):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = box.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.level = 0
        p.space_after = Pt(10)
        # bullet via prefix for reliable cross-platform look
        run = p.add_run()
        run.text = f"▸  {line}"
        _set_run(run, size=size, color=INK)
    return box


def _card(slide, x, y, w, h, title, body_lines, title_color=TEAL):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h)
    )
    _fill(shape, WHITE)
    shape.line.color.rgb = RGBColor(0xD7, 0xE0, 0xDC)
    shape.adjustments[0] = 0.08

    tbox = slide.shapes.add_textbox(Inches(x + 0.2), Inches(y + 0.15), Inches(w - 0.4), Inches(0.4))
    p = tbox.text_frame.paragraphs[0]
    run = p.add_run()
    run.text = title
    _set_run(run, size=16, bold=True, color=title_color)

    bbox = slide.shapes.add_textbox(Inches(x + 0.2), Inches(y + 0.55), Inches(w - 0.4), Inches(h - 0.7))
    tf = bbox.text_frame
    tf.word_wrap = True
    for i, line in enumerate(body_lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(4)
        run = p.add_run()
        run.text = line
        _set_run(run, size=13, color=INK)
    return shape


def _add_table(slide, rows, left, top, width, height):
    table_shape = slide.shapes.add_table(len(rows), len(rows[0]), Inches(left), Inches(top), Inches(width), Inches(height))
    table = table_shape.table
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            cell = table.cell(r, c)
            cell.text = str(val)
            for p in cell.text_frame.paragraphs:
                p.alignment = PP_ALIGN.CENTER
                for run in p.runs:
                    if r == 0:
                        _set_run(run, size=12, bold=True, color=WHITE)
                    else:
                        _set_run(run, size=12, color=INK)
            # fill
            fill = cell.fill
            fill.solid()
            if r == 0:
                fill.fore_color.rgb = NAVY
            elif r % 2 == 0:
                fill.fore_color.rgb = TEAL_LIGHT
            else:
                fill.fore_color.rgb = WHITE
    return table_shape


def build_pptx():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    slides_meta = []  # collect builders then assign page numbers

    def title_slide():
        s = _blank_slide(prs)
        # full navy background
        bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        _fill(bg, NAVY)
        # teal diagonal-ish band
        band = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(5.6), Inches(13.333), Inches(1.9))
        _fill(band, TEAL)

        t = s.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.5), Inches(1.2))
        p = t.text_frame.paragraphs[0]
        run = p.add_run()
        run.text = "Müasir Data Strukturları və Alqoritmlər"
        _set_run(run, size=36, bold=True, color=WHITE)

        sub = s.shapes.add_textbox(Inches(0.8), Inches(3.1), Inches(11.5), Inches(1.2))
        tf = sub.text_frame
        p = tf.paragraphs[0]
        run = p.add_run()
        run.text = "Sərbəst iş  ·  Mövzu 1–5  ·  Konsol tətbiqi"
        _set_run(run, size=20, color=TEAL_LIGHT)

        p = tf.add_paragraph()
        p.space_before = Pt(18)
        run = p.add_run()
        run.text = "Səid Abdullayev  ·  Nicat İbrahimov  ·  Yunus Həşimov"
        _set_run(run, size=18, color=WHITE)

        foot = s.shapes.add_textbox(Inches(0.8), Inches(6.15), Inches(11.5), Inches(0.8))
        p = foot.text_frame.paragraphs[0]
        run = p.add_run()
        run.text = "github.com/Abdullaeff1/dsa-serbest-is"
        _set_run(run, size=16, color=WHITE)
        return s

    def content(title, bullets, size=19):
        s = _blank_slide(prs)
        _bg(s, SAND)
        _sidebar(s)
        _top_band(s, title)
        _bullets(s, bullets, size=size)
        return s

    def cards_slide(title, cards):
        s = _blank_slide(prs)
        _bg(s, SAND)
        _sidebar(s)
        _top_band(s, title)
        # 3 cards
        w = 3.8
        gap = 0.25
        start = 0.55
        for i, (ct, lines) in enumerate(cards):
            _card(s, start + i * (w + gap), 1.55, w, 4.8, ct, lines)
        return s

    # Build slides
    title_slide()

    content(
        "Məqsəd və tapşırıq",
        [
            "5 mövzunu əhatə edən kiçik konsol tətbiqi hazırlamaq",
            "Strukturları özümüz implementasiya etmək (hazır list/dict əsas deyil)",
            "Performans müqayisəsi + mürəkkəblik (Big-O) izahı",
            "Hər strukturun tətbiqdə niyə seçildiyini göstərmək",
            "Komanda işi Git tarixçəsində görünməlidir",
        ],
    )

    content(
        "Tətbiqin funksiyaları (main.py menyusu)",
        [
            "1–5: Array, Linked List, SQD, Hash Table, BST demo-ları",
            "6: Bracket Checker — Stack ilə mötərizə yoxlama",
            "7: Ticket Line — Queue ilə növbə (FIFO)",
            "8: Music Playlist — Deque ilə ön/son əlavə",
            "9: Benchmark-ları işə sal (nəticə results/-ə yazılır)",
            "10: Avtomatik testləri işə sal",
            "İşə salma: python main.py",
        ],
        size=18,
    )

    # WHY structures — key teacher requirement
    s = _blank_slide(prs)
    _bg(s, SAND)
    _sidebar(s)
    _top_band(s, "Niyə bu strukturlar? (seçim izahı)")
    why = [
        ("Stack → Bracket Checker", [
            "Son açılan mötərizə ilk bağlanmalıdır",
            "Bu LIFO qaydasıdır → Stack ideal seçimdir",
            "Push/pop O(1) — sadə və sürətli",
        ]),
        ("Queue → Ticket Line", [
            "İlk gələn ilk xidmət alır (FIFO)",
            "Queue enqueue/dequeue ucları O(1)",
            "Ədalətli növbə modeli",
        ]),
        ("Deque → Playlist", [
            "Həm önə, həm sona mahnı əlavə lazımdır",
            "Deque hər iki ucda O(1)",
            "List ortası üçün lazım deyil",
        ]),
    ]
    for i, (ct, lines) in enumerate(why):
        _card(s, 0.55 + i * 4.15, 1.5, 3.95, 4.9, ct, lines)

    content(
        "Layihə arxitekturası",
        [
            "structures/ — Array, LinkedList, Stack/Queue/Deque, Hash, BST",
            "apps/ — 3 mini-tətbiq (Bracket, Ticket, Playlist)",
            "benchmarks/ — time.perf_counter_ns() ölçmələri",
            "tests/ — düzgünlük yoxlamaları",
            "docs/ — hesabat + təqdimat",
        ],
    )

    content(
        "Mövzu 1: Array və Dynamic Array",
        [
            "FixedArray — sabit tutum; dolanda OverflowError",
            "DynamicArray — dolanda capacity ×2 (doubling)",
            "Append sonda: Fixed O(1), Dynamic amortized O(1)",
            "Ortada insert və search: O(n)",
            "Eksperiment: n = 100, 1000, 5000 üzərində vaxt ölçülüb",
        ],
    )

    # Array table slide
    s = _blank_slide(prs)
    _bg(s, SAND)
    _sidebar(s)
    _top_band(s, "Array performans cədvəli (µs)")
    rows = [
        ["n", "Fixed append", "Dynamic append", "Insert orta", "Search"],
        ["100", "22", "42", "6", "5"],
        ["1000", "168", "199", "34", "45"],
        ["5000", "818", "1060", "148", "208"],
    ]
    _add_table(s, rows, 0.7, 1.7, 11.8, 3.2)
    note = s.shapes.add_textbox(Inches(0.7), Inches(5.2), Inches(11.8), Inches(1.2))
    tf = note.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = "Nəticə: DynamicArray append Fixed-ə yaxın qalır (amortized O(1)), amma Fixed dolanda dayanır. Ortada insert və search n artdıqca bahalaşır."
    _set_run(run, size=16, color=INK)

    content(
        "Mövzu 2: Singly vs Doubly Linked List",
        [
            "Singly: yalnız next → insert_back O(n)",
            "Doubly: prev + next + tail → hər iki ucda O(1)",
            "Trade-off: Doubly sürətli uclar, amma hər düyündə əlavə yaddaş",
            "n=5000: Singly insert_back ~223000 µs, Doubly ~1420 µs",
        ],
    )

    # List comparison table
    s = _blank_slide(prs)
    _bg(s, SAND)
    _sidebar(s)
    _top_band(s, "Linked List müqayisə cədvəli (µs)")
    rows = [
        ["n", "Singly front", "Singly back", "Doubly front", "Doubly back"],
        ["100", "106", "266", "208", "63"],
        ["1000", "620", "9076", "320", "816"],
        ["5000", "1295", "223014", "1480", "1420"],
    ]
    _add_table(s, rows, 0.55, 1.7, 12.1, 3.2)
    note = s.shapes.add_textbox(Inches(0.7), Inches(5.2), Inches(11.8), Inches(1.2))
    p = note.text_frame.paragraphs[0]
    run = p.add_run()
    run.text = "Nəticə: sonda əməliyyat üçün Doubly Linked List aydın üstündür. Queue/Deque-ni buna görə Doubly üzərində qurduq."
    _set_run(run, size=16, color=INK)

    content(
        "Mövzu 3: Stack, Queue, Deque",
        [
            "Stack (LIFO) — DynamicArray üzərində",
            "Queue (FIFO) — DoublyLinkedList",
            "Deque — hər iki ucda əlavə/silmə O(1)",
            "Hər biri tətbiqin ayrı funksiyasında istifadə olunur (aşağıda)",
        ],
    )

    s = cards_slide(
        "Mini-tətbiqlər (funksiya + struktur)",
        [
            ("Bracket Checker", [
                "Struktur: Stack",
                "Niyə: LIFO",
                "()[]{} tarazlığı",
                "Push açılan,",
                "pop bağlanan",
            ]),
            ("Ticket Line", [
                "Struktur: Queue",
                "Niyə: FIFO",
                "Müştəri növbəsi",
                "enqueue → gözlə",
                "dequeue → xidmət",
            ]),
            ("Music Playlist", [
                "Struktur: Deque",
                "Niyə: iki uc",
                "Önə/sona əlavə",
                "play_next = front",
                "remove_last = back",
            ]),
        ],
    )

    content(
        "Mövzu 4: Hash Table (chaining)",
        [
            "Öz hash table-ımız: hər bucket (key, value) siyahısıdır",
            "Collision → eyni bucket-ə zəncir (chaining)",
            "Load factor ~0.75 → capacity ikiqat artır, rehash",
            "Ortalama get/put O(1); worst-case O(n)",
            "Benchmark: böyük n-də get linear axtarışdan daha sabitdir",
        ],
    )

    content(
        "Mövzu 5: BST və balans problemi",
        [
            "Insert / search / delete / inorder / height implementasiya olunub",
            "Sıralı insert (1..n): ağac linked list-ə oxşayır → height ≈ n−1",
            "Təsadüfi insert: height adətən O(log n) səviyyəsində",
            "n=5000: sorted height=4999, random height≈28",
            "Axtarış da buna görə sorted-də xeyli yavaşlaya bilər",
        ],
    )

    # BST table
    s = _blank_slide(prs)
    _bg(s, SAND)
    _sidebar(s)
    _top_band(s, "BST: sorted vs random (balans)")
    rows = [
        ["n", "Sorted height", "Random height", "Sorted search µs", "Random search µs"],
        ["100", "99", "10", "5–8", "~1"],
        ["1000", "999", "20", "~37–90", "~2–5"],
        ["5000", "4999", "28", "~190–210", "~2–3"],
    ]
    _add_table(s, rows, 0.4, 1.7, 12.4, 3.2)
    note = s.shapes.add_textbox(Inches(0.7), Inches(5.2), Inches(11.8), Inches(1.2))
    p = note.text_frame.paragraphs[0]
    run = p.add_run()
    run.text = "İzah: sıralanmış verilənlər BST-ni degenerasiya edir. Real sistemlərdə AVL/Red-Black kimi balanslı ağaclar buna görə lazımdır."
    _set_run(run, size=16, color=INK)

    content(
        "Trade-off-lar",
        [
            "Array — indeks sürətli; ortada insert bahalı",
            "Linked list — uclar rahat; təsadüfi indeks yoxdur",
            "Hash — ortalama sürətli; worst-case və yaxşı hash lazımdır",
            "BST — sıralı axtarış üçün yaxşı; balans olmadan riskli",
            "Seçim həmişə məsələnin ehtiyacına görədir",
        ],
    )

    content(
        "Komanda rolları",
        [
            "Səid Abdullayev — Array, Hash Table, main.py, testlər",
            "Nicat İbrahimov — Linked List, Stack/Queue/Deque, mini-tətbiqlər",
            "Yunus Həşimov — BST, benchmark, sənədləşdirmə",
            "Git: git shortlog -sn  →  3 fərqli author görünür",
        ],
    )

    # Closing
    s = _blank_slide(prs)
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    _fill(bg, NAVY)
    band = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(0), Inches(13.333), Inches(0.18))
    _fill(band, TEAL)
    t = s.shapes.add_textbox(Inches(0.8), Inches(2.2), Inches(11.5), Inches(1))
    p = t.text_frame.paragraphs[0]
    run = p.add_run()
    run.text = "Nəticə"
    _set_run(run, size=36, bold=True, color=WHITE)
    body = s.shapes.add_textbox(Inches(0.8), Inches(3.3), Inches(11.5), Inches(2.5))
    tf = body.text_frame
    for i, line in enumerate(
        [
            "Mövzu 1–5 implementasiya + demo + benchmark tamamlanıb",
            "Hər strukturun tətbiqdə seçimi izah olunub",
            "Repo: github.com/Abdullaeff1/dsa-serbest-is",
            "Suallar?",
        ]
    ):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(8)
        run = p.add_run()
        run.text = f"▸  {line}"
        _set_run(run, size=18, color=TEAL_LIGHT)

    # Add footers to non-title/closing content slides
    total = len(prs.slides)
    for i, slide in enumerate(prs.slides, 1):
        # skip full-bleed title (1) and closing (last) for small footer style — still add page on content
        if i == 1 or i == total:
            continue
        _footer(slide, i, total)

    out = DOCS / "teqdimat.pptx"
    prs.save(out)
    print("Wrote", out, "slides=", total)
    return out


def _register_font():
    candidates = [
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\calibri.ttf",
        r"C:\Windows\Fonts\segoeui.ttf",
    ]
    for path in candidates:
        if os.path.isfile(path):
            pdfmetrics.registerFont(TTFont("AppFont", path))
            bold = (
                path.replace("arial.ttf", "arialbd.ttf")
                .replace("calibri.ttf", "calibrib.ttf")
                .replace("segoeui.ttf", "segoeuib.ttf")
            )
            if os.path.isfile(bold):
                pdfmetrics.registerFont(TTFont("AppFont-Bold", bold))
            else:
                pdfmetrics.registerFont(TTFont("AppFont-Bold", path))
            return "AppFont"
    return "Helvetica"


def build_pdf():
    font = _register_font()
    out = DOCS / "hesabat.pdf"
    doc = SimpleDocTemplate(
        str(out),
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "AZTitle",
        parent=styles["Heading1"],
        fontName=f"{font}-Bold" if font != "Helvetica" else "Helvetica-Bold",
        fontSize=16,
        spaceAfter=12,
        leading=20,
    )
    h2 = ParagraphStyle(
        "AZH2",
        parent=styles["Heading2"],
        fontName=f"{font}-Bold" if font != "Helvetica" else "Helvetica-Bold",
        fontSize=12,
        spaceBefore=14,
        spaceAfter=8,
        leading=16,
    )
    body = ParagraphStyle(
        "AZBody",
        parent=styles["Normal"],
        fontName=font,
        fontSize=10,
        leading=14,
        spaceAfter=6,
    )

    story = []
    story.append(Paragraph("Texniki hesabat — Sərbəst iş (Mövzu 1–5)", title))
    story.append(
        Paragraph(
            "<b>Fənn:</b> Müasir Data Strukturları və Alqoritmlər<br/>"
            "<b>Komanda:</b> Səid Abdullayev, Nicat İbrahimov, Yunus Həşimov<br/>"
            "<b>Repo:</b> https://github.com/Abdullaeff1/dsa-serbest-is",
            body,
        )
    )

    story.append(Paragraph("1. Problem və məqsəd", h2))
    story.append(
        Paragraph(
            "Kursun ilk 5 sərbəst iş mövzusu üzrə əsas data strukturlarını "
            "öz implementasiyamız ilə öyrənmək, mürəkkəblik izahı vermək, "
            "test və benchmark aparmaq, Stack/Queue/Deque üçün mini-tətbiq "
            "göstərmək tələb olunur.",
            body,
        )
    )

    story.append(Paragraph("2. Struktur seçimi (niyə?)", h2))
    for text in [
        "<b>Stack → Bracket Checker:</b> mötərizə tarazlığı LIFO tələb edir.",
        "<b>Queue → Ticket Line:</b> növbə FIFO ilə ədalətli xidmət verir.",
        "<b>Deque → Playlist:</b> həm önə, həm sona əlavə lazımdır.",
        "<b>Doubly list → Queue/Deque backend:</b> uclar O(1) olmalıdır.",
        "<b>Hash Table:</b> açar-dəyər axtarışı üçün ortalama O(1).",
        "<b>BST:</b> sıralı axtarış və balans probleminin nümayişi üçün.",
    ]:
        story.append(Paragraph(text, body))

    story.append(Paragraph("3. Mövzular üzrə qısa izah", h2))
    for text in [
        "<b>Mövzu 1:</b> FixedArray sabit tutumlu; DynamicArray dolanda capacity-ni ikiqat artırır.",
        "<b>Mövzu 2:</b> Singly sonda O(n), Doubly (tail ilə) hər iki ucda O(1).",
        "<b>Mövzu 3:</b> Bracket Checker (Stack), Ticket Line (Queue), Music Playlist (Deque).",
        "<b>Mövzu 4:</b> Chaining Hash Table; load factor 0.75-də resize.",
        "<b>Mövzu 5:</b> BST; sıralı insert ağacı degenerasiya edir (balans problemi).",
    ]:
        story.append(Paragraph(text, body))

    story.append(Paragraph("4. Mürəkkəblik cədvəli", h2))
    data = [
        ["Struktur", "Search", "Insert", "Delete"],
        ["Fixed Array", "O(n)", "sonda O(1)*", "O(n)"],
        ["Dynamic Array", "O(n)", "amortized O(1)", "O(n)"],
        ["Singly LL", "O(n)", "baş O(1) / son O(n)", "baş O(1)"],
        ["Doubly LL", "O(n)", "hər uc O(1)", "hər uc O(1)"],
        ["Hash Table", "avg O(1)", "avg O(1)", "avg O(1)"],
        ["BST", "avg O(log n)", "avg O(log n)", "avg O(log n)"],
    ]
    table = Table(data, colWidths=[3.5 * cm, 3.5 * cm, 4.5 * cm, 3.5 * cm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0B2A3A")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    f"{font}-Bold" if font != "Helvetica" else "Helvetica-Bold",
                ),
                ("FONTNAME", (0, 1), (-1, -1), font),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.whitesmoke, colors.Color(0.9, 0.95, 0.94)],
                ),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(table)
    story.append(Paragraph("* Fixed Array dolu olanda əlavə mümkün deyil.", body))

    story.append(Paragraph("5. Benchmark nəticələri", h2))
    story.append(
        Paragraph(
            "n=5000: Singly insert_back ~223000 µs, Doubly insert_back ~1420 µs. "
            "BST sorted height=4999, random height≈28. "
            "HashTable get linear axtarışdan daha sabitdir. "
            "Tam cədvəl: results/benchmark_results.txt",
            body,
        )
    )

    story.append(Paragraph("6. Nəticə", h2))
    story.append(
        Paragraph(
            "Layihə mövzu 1–5 tələblərini ödəyir: implementasiya, mini-tətbiq, "
            "struktur seçimi izahı, mürəkkəblik və eksperimental müqayisə.",
            body,
        )
    )

    story.append(Paragraph("7. İstinadlar", h2))
    story.append(
        Paragraph(
            "1. Goodrich et al., Data Structures and Algorithms in Python<br/>"
            "2. Cormen et al., Introduction to Algorithms<br/>"
            "3. Kurs sillabusu — sərbəst iş mövzuları 1–5",
            body,
        )
    )

    doc.build(story)
    print("Wrote", out)
    return out


def build_pptx_pdf_note():
    font = _register_font()
    out = DOCS / "teqdimat.pdf"
    doc = SimpleDocTemplate(str(out), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm)
    styles = getSampleStyleSheet()
    h = ParagraphStyle(
        "PH",
        parent=styles["Heading1"],
        fontName=f"{font}-Bold" if font != "Helvetica" else "Helvetica-Bold",
        fontSize=14,
        spaceAfter=10,
    )
    b = ParagraphStyle("PB", parent=styles["Normal"], fontName=font, fontSize=10, leading=14)
    story = [
        Paragraph("Təqdimat (PDF nüsxə) — Mövzu 1–5", h),
        Paragraph(
            "Əsas fayl: docs/teqdimat.pptx (dizaynlı slaydlar). "
            "Bu PDF qısa məzmun xülasəsidir.",
            b,
        ),
        Spacer(1, 8),
        Paragraph(
            "Slaydlar: Titul · Məqsəd · Menyü funksiyaları · Niyə bu strukturlar · "
            "Arxitektura · Array · Array cədvəli · Linked List · LL cədvəli · "
            "SQD · Mini-tətbiqlər · Hash · BST · BST cədvəli · Trade-off · "
            "Komanda · Nəticə",
            b,
        ),
        Spacer(1, 8),
        Paragraph("Komanda: Səid Abdullayev, Nicat İbrahimov, Yunus Həşimov", b),
        Paragraph("Repo: https://github.com/Abdullaeff1/dsa-serbest-is", b),
    ]
    doc.build(story)
    print("Wrote", out)
    return out


if __name__ == "__main__":
    DOCS.mkdir(exist_ok=True)
    build_pptx()
    build_pdf()
    build_pptx_pdf_note()
