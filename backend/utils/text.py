import html
import re
import unicodedata


def sanitize_text(text: str) -> str:

    text = unicodedata.normalize(
        "NFKC",
        text or ""
    )

    replacements = {

        "\u2018": "'",
        "\u2019": "'",

        "\u201c": '"',
        "\u201d": '"',

        "\u2013": "-",
        "\u2014": "-",

        "\u2022": "-",

        "\u00a0": " ",
    }

    for old, new in replacements.items():
        text = text.replace(
            old,
            new
        )

    text = re.sub(
        r"[ \t]+\n",
        "\n",
        text
    )

    text = re.sub(
        r"\n{4,}",
        "\n\n\n",
        text
    )

    return text.strip()


def terms_to_list(
    terms: str
) -> list[str]:

    if not terms:
        return []

    return [
        item.strip(" \t\r\n-")
        for item in terms.split(";")
        if item.strip()
    ]


def html_preview(text: str) -> str:

    safe = html.escape(
        sanitize_text(text)
    )

    blocks = []

    for block in re.split(
        r"\n\s*\n",
        safe
    ):

        lines = [
            line.strip()
            for line in block.splitlines()
            if line.strip()
        ]

        if lines:

            blocks.append(
                f"<p>{'<br>'.join(lines)}</p>"
            )

    return "\n".join(blocks)