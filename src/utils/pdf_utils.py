from __future__ import annotations
import fitz  # PyMuPDF
from pathlib import Path
from typing import Tuple
from PIL import Image
import io
import pytesseract

MIN_TEXT_LEN_FOR_NO_OCR = 30

class PDFDocument:
    def __init__(self, doc: fitz.Document):
        self._doc = doc

    @property
    def page_count(self) -> int:
        return self._doc.page_count

    def get_page(self, index: int) -> fitz.Page:
        return self._doc.load_page(index)


def open_document(path: str) -> PDFDocument:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)
    doc = fitz.open(str(p))
    return PDFDocument(doc)


def extract_page_text(pdf: PDFDocument, page_index: int) -> Tuple[str, bool]:
    page = pdf.get_page(page_index)
    text = page.get_text("text") or ""
    needs_ocr = len(text.strip()) < MIN_TEXT_LEN_FOR_NO_OCR
    return text, needs_ocr


def render_page_image(pdf: PDFDocument, page_index: int, zoom: float = 2.0) -> Image.Image:
    page = pdf.get_page(page_index)
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return img


def render_page_thumbnail(pdf: PDFDocument, page_index: int, max_size: Tuple[int, int] = (200, 260)) -> Image.Image:
    img = render_page_image(pdf, page_index, zoom=0.6)
    img.thumbnail(max_size)
    return img


def ocr_page_image(img: Image.Image) -> str:
    try:
        return pytesseract.image_to_string(img, lang="eng")
    except Exception:
        return ""
