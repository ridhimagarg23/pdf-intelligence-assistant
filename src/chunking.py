import re

def build_sections(markdown_text):

    sections = []

    pattern = r"^(#+)\s+(.*)$"

    matches = list(
        re.finditer(
            pattern,
            markdown_text,
            re.MULTILINE
        )
    )

    if not matches:

        return [
            {
                "heading": "Document",
                "content": markdown_text
            }
        ]

    for i, match in enumerate(matches):

        heading = match.group(2).strip()

        start = match.end()

        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(markdown_text)

        content = markdown_text[
            start:end
        ].strip()

        if len(content) > 50:

            sections.append(
                {
                    "heading": heading,
                    "content": content
                }
            )

    return sections