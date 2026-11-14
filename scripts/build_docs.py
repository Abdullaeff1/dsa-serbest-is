"""Generate presentation PPTX and technical report PDF (Azerbaijani)."""

from __future__ import annotations

import os
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt

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


def _add_slide(prs, title, bullets):
    layout = prs.slide_layouts[1]  # title + content
    slide = prs.slides.add_slide(layout)
    slide.shapes.title.text = title
    body = slide.placeholders[1].text_frame
    body.clear()
    for i, line in enumerate(bullets):
        if i == 0:
            p = body.paragraphs[0]
        else:
            p = body.add_paragraph()
        p.text = line
        p.level = 0
        p.font.size = Pt(18)
    return slide


def build_pptx():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Title slide
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "Müasir Data Strukturları və Alqoritmlər"
    slide.placeholders[1].text = (
        "Sərbəst iş — Mövzu 1–5\n"
        "Səid Abdullayev · Nicat İbrahimov · Yunus Həşimov"
    )

    slides = [
        (
            "Məqsəd",
            [
                "Əsas data strukturlarını özümüz implementasiya etmək",
                "Test + benchmark + Big-O izahı",
                "Stack / Queue / Deque üçün mini-tətbiqlər",
                "Git tarixçəsində komanda töhfələrinin görünməsi",
            ],
        ),
        (
            "Layihə arxitekturası",
            [
                "structures/ — Array, List, SQD, Hash, BST",
                "apps/ — Bracket Checker, Ticket Line, Playlist",
                "benchmarks/ + tests/ + docs/",
                "İşə salma: python main.py",
            ],
        ),
        (
            "Mövzu 1: Array vs Dynamic Array",
            [
                "FixedArray — sabit tutum, dolanda OverflowError",
                "DynamicArray — dolanda capacity ×2 (doubling)",
                "Append sonda: Fixed O(1), Dynamic amortized O(1)",
                "Ortada insert / search: O(n)",
            ],
        ),
        (
            "Mövzu 2: Singly vs Doubly Linked List",
            [
                "Singly: yalnız next → insert_back O(n)",
                "Doubly: prev + next + tail → hər iki ucda O(1)",
                "Trade-off: Doubly daha sürətli uclar, amma əlavə yaddaş",
                "Benchmark: Singly insert_back böyük n-də çox yavaşdır",
            ],
        ),
        (
            "Mövzu 3: Stack / Queue / Deque",
            [
                "Stack (LIFO) — DynamicArray üzərində",
                "Queue (FIFO) — DoublyLinkedList",
                "Deque — hər iki ucda əlavə/silmə O(1)",
            ],
        ),
        (
            "Mini-tətbiqlər",
            [
                "Bracket Checker — mötərizə tarazlığı (Stack)",
                "Ticket Line — müştəri növbəsi FIFO (Queue)",
                "Music Playlist — ön/son əlavə (Deque)",
            ],
        ),
        (
            "Mövzu 4: Hash Table (chaining)",
            [
                "Hər bucket: (key, value) siyahısı",
                "Toqquşma → eyni bucket-ə zəncir",
                "Load factor ~0.75 → capacity ikiqat artır",
                "Ortalama get/put: O(1); worst-case: O(n)",
            ],
        ),
        (
            "Mövzu 5: BST + balans problemi",
            [
                "Insert / search / delete / inorder / height",
                "Sıralı insert → height ≈ n−1 (degenerasiya)",
                "Təsadüfi insert → height ≈ O(log n)",
                "Nəticə: balanslaşdırma (AVL və s.) niyə lazımdır",
            ],
        ),
        (
            "Testlər",
            [
                "tests/test_all.py — xarici framework yoxdur",
                "Boş struktur, overflow, collision, BST delete",
                "Mini-tətbiq ssenariləri",
                "Nəticə: bütün yoxlamalar keçir",
            ],
        ),
        (
            "Benchmark — əsas müşahidələr",
            [
                "Singly insert_back ≫ Doubly insert_back (böyük n)",
                "HashTable get linear axtarışdan sabit qalır",
                "BST sorted height=4999, random height≈28 (n=5000)",
                "Nəticələr: results/benchmark_results.txt",
            ],
        ),
        (
            "Trade-off-lar",
            [
                "Array — indeks sürətli, ortada insert bahalı",
                "Linked list — uclar rahat, təsadüfi indeks yoxdur",
                "Hash — ortalama sürətli, worst-case və hash key",
                "BST — sıralı data üçün yaxşı, balans olmadan riskli",
            ],
        ),
        (
            "Komanda rolları",
            [
                "Səid Abdullayev — Array, Hash Table, main.py, testlər",
                "Nicat İbrahimov — Linked List, SQD, mini-tətbiqlər",
                "Yunus Həşimov — BST, benchmark, README/hesabat",
                "Git: git shortlog -sn",
            ],
        ),
        (
            "Nəticə",
            [
                "Mövzu 1–5 tələbləri ödənilib",
                "İmplementasiya + demo + mürəkkəblik + benchmark",
                "Repo: github.com/Abdullaeff1/dsa-serbest-is",
                "Suallar?",
            ],
        ),
    ]

    for title, bullets in slides:
        _add_slide(prs, title, bullets)

    out = DOCS / "teqdimat.pptx"
    prs.save(out)
    print("Wrote", out)
    return out


def _register_font():
    """Prefer a Windows font with Azerbaijani glyphs."""
    candidates = [
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\calibri.ttf",
        r"C:\Windows\Fonts\segoeui.ttf",
    ]
    for path in candidates:
        if os.path.isfile(path):
            pdfmetrics.registerFont(TTFont("AppFont", path))
            bold = path.replace("arial.ttf", "arialbd.ttf").replace(
                "calibri.ttf", "calibrib.ttf"
            ).replace("segoeui.ttf", "segoeuib.ttf")
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

    story.append(Paragraph("2. Yanaşma", h2))
    story.append(
        Paragraph(
            "Dil: Python 3 (xarici paket yoxdur). Hər struktur ayrı modulda "
            "(structures/). Mini-tətbiqlər apps/ qovluğundadır. Ölçmələr "
            "time.perf_counter_ns() ilə aparılır.",
            body,
        )
    )

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
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e79")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), f"{font}-Bold" if font != "Helvetica" else "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), font),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey]),
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

    story.append(Paragraph("5. Benchmark nəticələri (nümunə)", h2))
    story.append(
        Paragraph(
            "n=5000 üçün: Singly insert_back ~ yüz minlərlə µs, Doubly insert_back "
            "isə bir neçə min µs səviyyəsində qalır. BST sorted height=4999, "
            "random height≈28. HashTable get linear axtarışdan daha sabitdir. "
            "Tam cədvəl: results/benchmark_results.txt",
            body,
        )
    )

    story.append(Paragraph("6. Trade-off-lar və nəticə", h2))
    story.append(
        Paragraph(
            "Struktur seçimi tapşırığa görədir: indeks üçün array, uclar üçün "
            "doubly list / deque, açar-dəyər üçün hash, sıralı axtarış üçün "
            "BST (balansla). Layihə mövzu 1–5 tələblərini ödəyir.",
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
    """Also export a short PDF twin of the presentation outline for LMS."""
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
            "Bu PDF, teqdimat.pptx ilə eyni məzmunun qısa nüsxəsidir. "
            "Əsas təqdimat faylı: docs/teqdimat.pptx",
            b,
        ),
        Spacer(1, 8),
        Paragraph(
            "Slaydlar: Titul · Məqsəd · Arxitektura · Array · Linked List · "
            "SQD · Mini-tətbiqlər · Hash · BST · Test · Benchmark · "
            "Trade-off · Komanda · Nəticə",
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
