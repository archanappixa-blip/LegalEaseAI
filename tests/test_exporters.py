from backend.services.exporters import (
    make_docx,
    make_pdf,
    make_txt,
)


def test_txt_export():

    stream = make_txt(
        "TITLE\nFreelance Work Contract"
    )

    data = stream.read()

    assert data.startswith(
        b"TITLE"
    )


def test_docx_export():

    stream = make_docx(
        "TITLE\nFreelance Work Contract"
    )

    data = stream.read()

    assert data[:2] == b"PK"


def test_pdf_export():

    stream = make_pdf(
        "TITLE\nFreelance Work Contract"
    )

    data = stream.read()

    assert data.startswith(
        b"%PDF"
    )