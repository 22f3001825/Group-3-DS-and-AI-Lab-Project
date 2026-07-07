"""
services/pdf_generator.py
────────────────────────────────────────────────────────────
Generates well-formatted lecture-note PDFs using ReportLab Platypus.
Supports both "simple" (concise) and "detailed" (deep-dive) note modes.
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate


# ── Brand colours ─────────────────────────────────────────────────────────────
BLUE_600  = HexColor("#2563eb")
BLUE_100  = HexColor("#dbeafe")
GRAY_800  = HexColor("#1f2937")
GRAY_600  = HexColor("#4b5563")
GRAY_200  = HexColor("#e5e7eb")
GRAY_50   = HexColor("#f9fafb")
PURPLE    = HexColor("#7c3aed")
GREEN     = HexColor("#059669")

MODE_COLOR = {
    "simple":   BLUE_600,
    "detailed": PURPLE,
}
MODE_LABEL = {
    "simple":   "Quick Notes (Simple)",
    "detailed": "Deep-Dive Notes (Detailed)",
}


def _note_html_to_reportlab(text: str) -> str:
    """
    Convert a note block (safe HTML produced by notes_generator: <strong>,
    <strong class="note-heading">, and <br>) into ReportLab mini-markup,
    which only understands a small tag subset via Paragraph().
    """
    if not isinstance(text, str):
        text = str(text)
    out = text.replace('<strong class="note-heading">', "<b>")
    out = out.replace("<strong>", "<b>").replace("</strong>", "</b>")
    out = out.replace("<br>", "<br/>")
    return out


# ── Styles ────────────────────────────────────────────────────────────────────

def _build_styles(detail_level: str):
    base = getSampleStyleSheet()
    accent = MODE_COLOR.get(detail_level, BLUE_600)

    cover_title = ParagraphStyle(
        "CoverTitle",
        fontName="Helvetica-Bold",
        fontSize=26,
        leading=32,
        textColor=white,
        alignment=TA_CENTER,
        spaceAfter=8,
    )
    cover_sub = ParagraphStyle(
        "CoverSub",
        fontName="Helvetica",
        fontSize=13,
        leading=18,
        textColor=HexColor("#c7d2fe"),
        alignment=TA_CENTER,
    )
    mode_badge = ParagraphStyle(
        "ModeBadge",
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=16,
        textColor=white,
        alignment=TA_CENTER,
        spaceAfter=4,
    )
    section_heading = ParagraphStyle(
        "SectionHeading",
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=18,
        textColor=GRAY_800,
        spaceBefore=4,
        spaceAfter=4,
    )
    timestamp_style = ParagraphStyle(
        "Timestamp",
        fontName="Courier-Bold",
        fontSize=9,
        leading=12,
        textColor=accent,
        spaceAfter=6,
    )
    bullet_style = ParagraphStyle(
        "Bullet",
        fontName="Helvetica",
        fontSize=11,
        leading=17,
        textColor=GRAY_600,
        leftIndent=4,
        spaceAfter=10,
        alignment=TA_JUSTIFY if detail_level == "detailed" else TA_LEFT,
    )
    footer_style = ParagraphStyle(
        "Footer",
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        textColor=HexColor("#9ca3af"),
        alignment=TA_CENTER,
    )
    toc_item = ParagraphStyle(
        "TOCItem",
        fontName="Helvetica",
        fontSize=10,
        leading=15,
        textColor=GRAY_600,
        leftIndent=8,
    )
    toc_header = ParagraphStyle(
        "TOCHeader",
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=GRAY_800,
        spaceAfter=8,
        spaceBefore=4,
    )
    return {
        "cover_title": cover_title,
        "cover_sub": cover_sub,
        "mode_badge": mode_badge,
        "section_heading": section_heading,
        "timestamp": timestamp_style,
        "bullet": bullet_style,
        "footer": footer_style,
        "toc_item": toc_item,
        "toc_header": toc_header,
        "accent": accent,
    }


# ── Header / Footer callback ──────────────────────────────────────────────────

def _make_header_footer(title: str, detail_level: str):
    accent = MODE_COLOR.get(detail_level, BLUE_600)

    def on_page(canvas, doc):
        w, h = A4
        canvas.saveState()

        # Top rule
        canvas.setStrokeColor(accent)
        canvas.setLineWidth(2)
        canvas.line(1.5 * cm, h - 1.2 * cm, w - 1.5 * cm, h - 1.2 * cm)

        # Header text
        canvas.setFont("Helvetica-Bold", 9)
        canvas.setFillColor(GRAY_600)
        canvas.drawString(1.5 * cm, h - 1.55 * cm, title[:70])
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(HexColor("#9ca3af"))
        canvas.drawRightString(w - 1.5 * cm, h - 1.55 * cm, f"Page {doc.page}")

        # Bottom rule
        canvas.setStrokeColor(GRAY_200)
        canvas.setLineWidth(0.5)
        canvas.line(1.5 * cm, 1.4 * cm, w - 1.5 * cm, 1.4 * cm)
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(HexColor("#9ca3af"))
        canvas.drawCentredString(w / 2, 1.0 * cm, "IIT Madras DS-AI Platform · Generated by DS-AI Notes")

        canvas.restoreState()

    return on_page


# ── Cover page ────────────────────────────────────────────────────────────────

def _build_cover(notes_data: dict, styles: dict) -> list:
    w, h = A4
    accent = styles["accent"]
    detail_level = notes_data.get("detail_level", "simple")
    mode_label = MODE_LABEL.get(detail_level, "Notes")

    # Blue cover banner (drawn via a coloured table)
    cover_bg = Table(
        [[Paragraph(notes_data.get("title", "Lecture Notes"), styles["cover_title"]),
          ""]],
        colWidths=[w - 3 * cm, 0],
    )
    cover_bg.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), accent),
        ("ROWPADDING", (0, 0), (-1, -1), 26),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("SPAN", (0, 0), (-1, -1)),
    ]))

    mode_tbl = Table(
        [[Paragraph(f"⚡ {mode_label}", styles["mode_badge"])]],
        colWidths=[w - 3 * cm],
    )
    mode_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), HexColor("#1d4ed8")),
        ("ROWPADDING", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    meta_rows = [
        ["Video ID:",    notes_data.get("video_id", "—")],
        ["Duration:",    notes_data.get("total_duration", "—")],
        ["Sections:",    str(len(notes_data.get("sections", [])))],
        ["Generated:",   datetime.now().strftime("%d %b %Y, %H:%M")],
    ]
    meta_tbl = Table(meta_rows, colWidths=[3 * cm, 10 * cm])
    meta_tbl.setStyle(TableStyle([
        ("FONTNAME",  (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME",  (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE",  (0, 0), (-1, -1), 10),
        ("TEXTCOLOR", (0, 0), (0, -1), GRAY_800),
        ("TEXTCOLOR", (1, 0), (1, -1), GRAY_600),
        ("ROWPADDING",(0, 0), (-1, -1), 5),
        ("LINEBELOW", (0, 0), (-1, -2), 0.3, GRAY_200),
    ]))

    return [
        cover_bg,
        Spacer(1, 0.4 * cm),
        mode_tbl,
        Spacer(1, 1 * cm),
        meta_tbl,
        PageBreak(),
    ]


# ── Table of Contents ─────────────────────────────────────────────────────────

def _build_toc(notes_data: dict, styles: dict) -> list:
    items = [Paragraph("Table of Contents", styles["toc_header"]),
             HRFlowable(width="100%", thickness=1, color=GRAY_200, spaceAfter=8)]
    for sec in notes_data.get("sections", []):
        items.append(
            Paragraph(
                f"<b>{sec['section_num']}.</b>&nbsp;&nbsp;{sec['title']}"
                f"&nbsp;&nbsp;<font color='#9ca3af'>{sec['timestamp']}</font>",
                styles["toc_item"],
            )
        )
    items.append(PageBreak())
    return items


# ── Section content ───────────────────────────────────────────────────────────

def _build_sections(notes_data: dict, styles: dict) -> list:
    accent = styles["accent"]
    detail_level = notes_data.get("detail_level", "simple")
    story = []

    for sec in notes_data.get("sections", []):
        # Section header block
        header_content = [
            [
                Paragraph(
                    f"<font color='white'><b> {sec['section_num']} </b></font>",
                    ParagraphStyle("Num", fontName="Helvetica-Bold", fontSize=12,
                                   textColor=white, alignment=TA_CENTER),
                ),
                Paragraph(
                    f"<b>{sec['title']}</b>",
                    ParagraphStyle("SH", fontName="Helvetica-Bold", fontSize=12,
                                   textColor=GRAY_800, leading=16),
                ),
                Paragraph(
                    f"▶ {sec['timestamp']}",
                    ParagraphStyle("TS", fontName="Courier-Bold", fontSize=9,
                                   textColor=accent, alignment=TA_LEFT),
                ),
            ]
        ]
        hdr_tbl = Table(header_content, colWidths=[1.0 * cm, 12 * cm, 3.5 * cm])
        hdr_tbl.setStyle(TableStyle([
            ("BACKGROUND",   (0, 0), (0, 0), accent),
            ("BACKGROUND",   (1, 0), (-1, 0), GRAY_50),
            ("ROWPADDING",   (0, 0), (-1, -1), 8),
            ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
            ("BOX",          (0, 0), (-1, -1), 0.5, GRAY_200),
            ("LINEAFTER",    (0, 0), (0, 0), 0.5, GRAY_200),
        ]))

        # Explanation blocks (already safe HTML from notes_generator: <strong>, <br>)
        bullet_items = []
        for b in sec.get("bullets", []):
            text = _note_html_to_reportlab(b)
            bullet_items.append(
                Paragraph(text, styles["bullet"])
            )

        if not bullet_items:
            bullet_items.append(
                Paragraph(
                    "<i>No key points extracted for this section.</i>",
                    styles["bullet"],
                )
            )

        block = KeepTogether([hdr_tbl, Spacer(1, 0.25 * cm)] + bullet_items + [Spacer(1, 0.6 * cm)])
        story.append(block)

    return story


# ── Public API ────────────────────────────────────────────────────────────────

def create_pdf(notes_data: dict, output_path: str) -> str:
    """
    Render notes_data to a formatted PDF at output_path.
    notes_data must contain keys: title, video_id, detail_level, total_duration, sections.
    Returns output_path on success.
    """
    detail_level = notes_data.get("detail_level", "simple")
    title = notes_data.get("title", "Lecture Notes")
    styles = _build_styles(detail_level)

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        topMargin=2.2 * cm,
        bottomMargin=2.0 * cm,
        title=title,
        author="DS-AI Platform",
        subject=f"{MODE_LABEL.get(detail_level, 'Notes')} — {notes_data.get('video_id', '')}",
    )

    on_page = _make_header_footer(title, detail_level)

    story = []
    story += _build_cover(notes_data, styles)
    story += _build_toc(notes_data, styles)
    story += _build_sections(notes_data, styles)

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    return output_path