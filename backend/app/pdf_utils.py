"""PDF extraction helpers for uploaded assignment files."""

from pathlib import Path

from PyPDF2 import PdfReader


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract readable text from every page in a PDF file."""

    reader = PdfReader(str(pdf_path))
    page_text: list[str] = []

    for page_number, page in enumerate(reader.pages, start=1):
        extracted = page.extract_text() or ""
        cleaned = extracted.strip()
        if cleaned:
            page_text.append(f"[Page {page_number}]\n{cleaned}")

    return "\n\n".join(page_text).strip()
