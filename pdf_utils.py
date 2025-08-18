# pdf_utils.py

def create_pdf(resume_content, filename):
    """
    Build a clean, fixed resume layout from AI/form text using ReportLab.
    - Fixed left-aligned contact line
    - Section headers not forced to UPPERCASE
    - Robust parsing for 'HEADER: first sentence...' lines
    - Safer email/phone detection (no C++ false positives)
    """
    import re
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, HRFlowable
    )
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib import colors
    import streamlit as st

    try:
        # ---------- helpers ----------
        EMAIL_RE = re.compile(r"\b[\w\.-]+@[\w\.-]+\.\w+\b")
        PHONE_RE = re.compile(r"\+?\d[\d\-\s\(\)]{7,}\d")  # + optional, 9+ digits total
        URL_RE = re.compile(r"\b(?:https?://|www\.)\S+\b", re.I)

        # Canonical section names & aliases (normalize to keys below)
        SECTION_ALIASES = {
            "PROFESSIONAL SUMMARY": "SUMMARY",
            "SUMMARY": "SUMMARY",
            "WORK EXPERIENCE": "EXPERIENCE",
            "EXPERIENCE": "EXPERIENCE",
            "EDUCATION": "EDUCATION",
            "SKILLS": "SKILLS",
            "TECHNICAL SKILLS": "SKILLS",
            "CORE SKILLS": "SKILLS",
            "CORE COMPETENCIES": "SKILLS",
            "CERTIFICATIONS": "CERTIFICATIONS",
            "PROJECTS": "PROJECTS",
            "NOTE": "NOTE",
            "NOTES": "NOTE",
        }
        CANON_ORDER = ["SUMMARY", "EXPERIENCE", "EDUCATION", "SKILLS", "CERTIFICATIONS", "PROJECTS", "NOTE"]

        def normalize_header(line):
            # Detect 'Header: text' or 'Header - text' and split cleanly
            m = re.match(r"^\s*([A-Za-z\s]+?)\s*[:\-–]\s*(.+)$", line)
            if m:
                return m.group(1).strip(), m.group(2).strip()
            return line.strip(), None

        def is_header(line):
            hdr, _ = normalize_header(line)
            return SECTION_ALIASES.get(hdr.upper(), None)

        def parse_text(text):
            """
            Returns:
              name (str or None),
              contacts (list[str]),
              sections (dict[str, dict])
              sections structure:
                - SUMMARY: {'paras': [..]}
                - SKILLS: {'lines': [..]}  (preserves 'Category: items' if present)
                - EXPERIENCE: {'entries': [{'header': 'Job | Company | Dates', 'bullets':[...]}], 'paras':[]}
                - EDUCATION/CERTIFICATIONS/PROJECTS: {'lines': [...], 'bullets': [...], 'paras': [...]}
                - NOTE: {'paras': [...]}
            """
            lines = [ln.strip() for ln in text.splitlines()]
            lines = [ln for ln in lines if ln]  # drop blanks

            name = None
            contacts = []
            sections = {k: {} for k in CANON_ORDER}
            for k in sections:
                sections[k] = {"paras": [], "lines": [], "bullets": [], "entries": []}

            current = None
            pending_header_text = None  # holds text after "HEADER: text"

            # --- header block (name + contacts) until first section header ---
            i = 0
            while i < len(lines):
                ln = lines[i]
                canon = is_header(ln)
                if canon:
                    # stop header block; process the header line in the main loop below
                    break

                # first non-empty non-contact line → name (once)
                if name is None and not EMAIL_RE.search(ln) and not PHONE_RE.search(ln) and not URL_RE.search(ln):
                    name = ln
                else:
                    # contact line: email/phone/url or explicit "Email: ...", "Phone: ..."
                    if EMAIL_RE.search(ln) or PHONE_RE.search(ln) or URL_RE.search(ln) or re.search(r"(?i)\b(email|phone|linkedin|github)\b", ln):
                        contacts.append(ln)
                    else:
                        # If extra fluff before sections, treat as summary paragraph fallback
                        sections["SUMMARY"]["paras"].append(ln)
                i += 1

            # --- main sections ---
            while i < len(lines):
                ln = lines[i]
                canon = is_header(ln)
                if canon:
                    # set current canonical section
                    hdr, after = normalize_header(ln)
                    current = SECTION_ALIASES[hdr.upper()]
                    pending_header_text = after  # if "HEADER: text" capture the text as first para
                    i += 1
                    continue

                if current is None:
                    # no recognized header yet; treat as summary
                    sections["SUMMARY"]["paras"].append(ln)
                    i += 1
                    continue

                # add the text that followed a "HEADER: text" line as first paragraph
                if pending_header_text:
                    sections[current]["paras"].append(pending_header_text)
                    pending_header_text = None

                # bullets
                if ln.startswith(("•", "-", "*")):
                    sections[current]["bullets"].append(ln.lstrip("•-* ").strip())
                    i += 1
                    continue

                # Experience: detect "Role | Company | Dates"
                if current == "EXPERIENCE" and "|" in ln:
                    parts = [p.strip() for p in ln.split("|")]
                    # Allow 2 or 3 parts
                    if len(parts) == 3:
                        header = f"{parts[0]} | {parts[1]} — {parts[2]}"
                    elif len(parts) == 2:
                        header = f"{parts[0]} — {parts[1]}"
                    else:
                        header = " | ".join(parts)
                    sections[current]["entries"].append({"header": header, "bullets": []})
                    i += 1
                    # consume following bullets for this entry
                    while i < len(lines) and lines[i].strip().startswith(("•", "-", "*")):
                        sections[current]["entries"][-1]["bullets"].append(lines[i].strip().lstrip("•-* ").strip())
                        i += 1
                    continue

                # Skills: keep 'Category: items' as lines; otherwise comma list
                if current == "SKILLS":
                    sections[current]["lines"].append(ln)
                    i += 1
                    continue

                # default: paragraph or line
                sections[current]["paras"].append(ln)
                i += 1

            return name, contacts, sections

        # ---------- document + styles ----------
        doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            topMargin=0.5 * inch,
            bottomMargin=0.5 * inch,
            leftMargin=0.75 * inch,
            rightMargin=0.75 * inch,
        )
        styles = getSampleStyleSheet()

        # Base body text
        body = ParagraphStyle(
            "Body",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=13,
            textColor=colors.HexColor("#1f2937"),
            alignment=TA_LEFT,
            spaceAfter=4,
        )
        # Name (left-aligned, bigger)
        name_style = ParagraphStyle(
            "Name",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=20,
            textColor=colors.HexColor("#111827"),
            alignment=TA_LEFT,
            spaceAfter=2,
        )
        # Contact line (left, small)
        contact_style = ParagraphStyle(
            "Contact",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=12,
            textColor=colors.HexColor("#4b5563"),
            alignment=TA_LEFT,
            spaceAfter=8,
        )
        # Section header (no forced UPPERCASE)
        section_header = ParagraphStyle(
            "SectionHeader",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12.5,
            leading=14,
            textColor=colors.HexColor("#111827"),
            spaceBefore=10,
            spaceAfter=4,
        )
        # Bullet body
        bullet = ParagraphStyle(
            "Bullet",
            parent=body,
            leftIndent=16,
            bulletIndent=8,
            spaceAfter=2,
        )
        # Experience entry header
        job_header = ParagraphStyle(
            "JobHeader",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=13,
            textColor=colors.HexColor("#111827"),
            spaceBefore=4,
            spaceAfter=2,
        )
        # Note style (small, italic, not bold/caps)
        note_style = ParagraphStyle(
            "Note",
            parent=styles["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#6b7280"),
            alignment=TA_LEFT,
            spaceBefore=8,
        )

        # ---------- build content ----------
        name, contacts, sections = parse_text(resume_content)
        story = []

        # Name
        if name:
            story.append(Paragraph(name, name_style))
        # Contact — join with separators, left-aligned
        if contacts:
            # Deduplicate and keep order
            seen = set()
            clean = []
            for c in contacts:
                if c not in seen:
                    seen.add(c)
                    clean.append(c)
            story.append(Paragraph("  |  ".join(clean), contact_style))

        # Subtle divider
        story.append(HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#e5e7eb")))
        story.append(Spacer(1, 6))

        # Sections in fixed order for consistent template
        for key in CANON_ORDER:
            sec = sections.get(key)
            if not sec:
                continue
            # Decide if section has any content
            has_content = any([sec["paras"], sec["lines"], sec["bullets"], sec["entries"]])
            if not has_content:
                continue

            # Header (as-is, not uppercased)
            story.append(Paragraph(key.title() if key != "NOTE" else "Note", section_header))

            # Render by type
            if key == "SUMMARY":
                for p in sec["paras"]:
                    story.append(Paragraph(p, body))

            elif key == "EXPERIENCE":
                # Structured entries if present
                if sec["entries"]:
                    for entry in sec["entries"]:
                        story.append(Paragraph(entry["header"], job_header))
                        for btxt in entry["bullets"]:
                            story.append(Paragraph(f"• {btxt}", bullet))
                # Any extra bullets outside structured entries
                for btxt in sec["bullets"]:
                    story.append(Paragraph(f"• {btxt}", bullet))
                # Any paras that weren't captured
                for p in sec["paras"]:
                    story.append(Paragraph(p, body))

            elif key == "SKILLS":
                # Prefer categorized lines like "Languages: Python, Java"
                if sec["lines"]:
                    for ln in sec["lines"]:
                        if ":" in ln:
                            cat, items = ln.split(":", 1)
                            story.append(Paragraph(f"<b>{cat.strip()}:</b> {items.strip()}", body))
                        else:
                            story.append(Paragraph(ln, body))
                # Or bullets
                for btxt in sec["bullets"]:
                    story.append(Paragraph(f"• {btxt}", bullet))
                for p in sec["paras"]:
                    story.append(Paragraph(p, body))

            elif key in ("EDUCATION", "CERTIFICATIONS", "PROJECTS"):
                # Print lines first (often 'Degree | School | Year')
                for ln in sec["lines"]:
                    story.append(Paragraph(ln, body))
                for btxt in sec["bullets"]:
                    story.append(Paragraph(f"• {btxt}", bullet))
                for p in sec["paras"]:
                    story.append(Paragraph(p, body))

            elif key == "NOTE":
                # Only light, italic, not bold/caps
                for p in sec["paras"]:
                    story.append(Paragraph(p, note_style))

            # small spacing after each section
            story.append(Spacer(1, 4))

        # ---------- build PDF ----------
        doc.build(story)
        return True

    except Exception as e:
        st.error(f"Error creating PDF: {str(e)}")
        return False
