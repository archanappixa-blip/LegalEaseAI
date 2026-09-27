import os
from io import BytesIO

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt
from fpdf import FPDF

from backend.utils.text import sanitize_text


# =========================================================
# LOGO
# =========================================================

LOGO_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "assets",
        "logo.png"
    )
)


# =========================================================
# TXT
# =========================================================

def make_txt(text: str) -> bytes:
    return sanitize_text(text).encode("utf-8")


# =========================================================
# DOCX
# =========================================================

def make_docx(
    text: str,
    document_type: str = "Legal Document",
    terms: str = "",
    brand_name: str = "LegalEase"
) -> bytes:

    doc = Document()

    section = doc.sections[0]

    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

    # Header
    header = section.header

    header_paragraph = header.paragraphs[0]
    header_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    if os.path.exists(LOGO_PATH):

        run = header_paragraph.add_run()

        run.add_picture(
            LOGO_PATH,
            width=Inches(1.5)
        )

    # Brand
    brand_paragraph = doc.add_paragraph()
    brand_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    run = brand_paragraph.add_run(brand_name)
    run.bold = True
    run.font.size = Pt(20)

    # Title
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    run = title.add_run(document_type.upper())
    run.bold = True
    run.font.size = Pt(16)

    # Content
    clean_text = sanitize_text(text)

    for line in clean_text.splitlines():

        line = line.strip()

        if not line:
            doc.add_paragraph()
            continue

        paragraph = doc.add_paragraph()
        paragraph.paragraph_format.space_after = Pt(8)

        run = paragraph.add_run(line)
        run.font.size = Pt(11)

    # Terms
    if terms.strip():

        terms_title = doc.add_paragraph()

        run = terms_title.add_run("Terms")
        run.bold = True
        run.font.size = Pt(12)

        for term in terms.split(";"):

            term = term.strip()

            if term:

                paragraph = doc.add_paragraph(
                    style="List Bullet"
                )

                paragraph.add_run(term)

    # Footer
    footer = section.footer

    footer_paragraph = footer.paragraphs[0]
    footer_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER

    footer_run = footer_paragraph.add_run(
        f"{brand_name} | "
        f"AI-assisted draft | "
        f"Not legal advice"
    )

    footer_run.font.size = Pt(9)

    output = BytesIO()

    doc.save(output)

    return output.getvalue()


# =========================================================
# PDF CLASS
# =========================================================

class LegalPDF(FPDF):

    def __init__(
        self,
        brand_name="LegalEase",
        document_type="Legal Document"
    ):

        super().__init__(
            orientation="P",
            unit="mm",
            format="A4"
        )

        self.brand_name = brand_name
        self.document_type = document_type

        self.set_margins(
            left=20,
            top=42,
            right=20
        )

        self.set_auto_page_break(
            auto=True,
            margin=20
        )

    # -----------------------------------------------------
    # HEADER
    # -----------------------------------------------------

    def header(self):

        if os.path.exists(LOGO_PATH):

            try:

                logo_width = 35

                x_position = (
                    self.w - logo_width
                ) / 2

                self.image(
                    LOGO_PATH,
                    x=x_position,
                    y=8,
                    w=logo_width
                )

            except Exception:
                pass

        self.set_y(30)

        self.set_font(
            "Arial",
            "B",
            14
        )

        self.cell(
            0,
            7,
            self.brand_name,
            new_x="LMARGIN",
            new_y="NEXT",
            align="C"
        )

        self.set_font(
            "Arial",
            "B",
            11
        )

        self.cell(
            0,
            6,
            self.document_type,
            new_x="LMARGIN",
            new_y="NEXT",
            align="C"
        )

        self.ln(5)

    # -----------------------------------------------------
    # FOOTER
    # -----------------------------------------------------

    def footer(self):

        self.set_y(-15)

        self.set_font(
            "Arial",
            "",
            8
        )

        self.cell(
            0,
            10,
            (
                f"{self.brand_name} | "
                f"AI-assisted draft | "
                f"Not legal advice | "
                f"Page {self.page_no()}"
            ),
            align="C"
        )


# =========================================================
# SAFE PDF TEXT
# =========================================================

def safe_pdf_text(text: str) -> str:

    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2026": "...",
        "\u00a0": " ",
        "\u2022": "-",
        "\u00b7": "-",
        "\t": " "
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return (
        text
        .encode(
            "latin-1",
            "replace"
        )
        .decode("latin-1")
    )


# =========================================================
# WRITE SAFE TEXT
# =========================================================

def write_pdf_text(
    pdf,
    text,
    height=6,
    bold=False
):

    text = safe_pdf_text(text)

    if not text.strip():
        pdf.ln(4)
        return

    if bold:

        pdf.set_font(
            "Arial",
            "B",
            11
        )

    else:

        pdf.set_font(
            "Arial",
            "",
            11
        )

    # IMPORTANT:
    # wrapmode="CHAR" prevents the
    # "Not enough horizontal space"
    # error caused by long words/strings.

    pdf.multi_cell(
        w=pdf.epw,
        h=height,
        text=text,
        border=0,
        align="L",
        fill=False,
        new_x="LMARGIN",
        new_y="NEXT",
        wrapmode="CHAR"
    )


# =========================================================
# PDF EXPORT
# =========================================================

def make_pdf(
    text: str,
    document_type: str = "Legal Document",
    terms: str = "",
    brand_name: str = "LegalEase"
) -> bytes:

    pdf = LegalPDF(
        brand_name=brand_name,
        document_type=document_type
    )

    pdf.set_title(
        f"{brand_name} - {document_type}"
    )

    pdf.set_author(
        brand_name
    )

    pdf.add_page()

    # -----------------------------------------------------
    # MAIN DOCUMENT
    # -----------------------------------------------------

    clean_text = sanitize_text(text)

    for line in clean_text.splitlines():

        line = line.strip()

        if not line:

            pdf.ln(4)

            continue

        is_heading = (
            line.endswith(":")
            or (
                len(line) >= 2
                and line[0].isdigit()
                and line[1] == "."
            )
        )

        write_pdf_text(
            pdf,
            line,
            height=7 if is_heading else 6,
            bold=is_heading
        )

        pdf.ln(1)

    # -----------------------------------------------------
    # TERMS
    # -----------------------------------------------------

    if terms.strip():

        pdf.ln(3)

        write_pdf_text(
            pdf,
            "Terms:",
            height=7,
            bold=True
        )

        for term in terms.split(";"):

            term = term.strip()

            if not term:
                continue

            write_pdf_text(
                pdf,
                "- " + term,
                height=6,
                bold=False
            )

            pdf.ln(1)

    # -----------------------------------------------------
    # OUTPUT
    # -----------------------------------------------------

    result = pdf.output()

    if isinstance(result, bytearray):
        result = bytes(result)

    if isinstance(result, str):
        result = result.encode("latin-1")

    return result