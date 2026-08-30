from pathlib import Path

from pypdf import PdfReader
from docx import Document


def extract_text_from_document(file_path: str) -> str:
    """
    Extract text from TXT, PDF, or DOCX files.
    """

    path = Path(file_path)
    extension = path.suffix.lower()

    if extension == ".txt":
        return path.read_text(encoding="utf-8")

    if extension == ".pdf":
        reader = PdfReader(str(path))

        text = []

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text.append(page_text)

        return "\n".join(text)

    if extension == ".docx":
        document = Document(str(path))

        text = []

        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                text.append(paragraph.text)

        return "\n".join(text)

    raise ValueError(
        "Unsupported file type. Please use TXT, PDF, or DOCX."
    )