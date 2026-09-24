from backend.services.exporters import (
    make_docx,
    make_pdf,
    make_txt
)


SAMPLE_DOCUMENT = """
FREELANCE WORK CONTRACT

1. PARTIES

Jane Doe (Service Provider)
and
TechNova Inc. (Client).

2. PAYMENT

Payment is due within 30 days
of invoice.

3. CONFIDENTIALITY

Confidential information must
be protected.

DRAFT FOR REVIEW - NOT LEGAL ADVICE
""".strip()


def test_txt_export():

    result = make_txt(
        SAMPLE_DOCUMENT
    )

    assert result.startswith(
        b"FREELANCE WORK CONTRACT"
    )

    assert (
        b"NOT LEGAL ADVICE"
        in result
    )


def test_docx_export():

    result = make_docx(

        SAMPLE_DOCUMENT,

        "Freelance Work Contract",

        (
            "Payment within 30 days;"
            "Confidentiality"
        ),

        "LegalEase"
    )

    # DOCX files are ZIP containers

    assert result[:2] == b"PK"


def test_pdf_export():

    result = make_pdf(

        SAMPLE_DOCUMENT,

        "Freelance Work Contract",

        (
            "Payment within 30 days;"
            "Confidentiality"
        ),

        "LegalEase"
    )

    assert result.startswith(
        b"%PDF"
    )