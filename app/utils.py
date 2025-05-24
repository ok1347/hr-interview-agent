#this module provides utility functions for text extraction from PDF files.

import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

def extract_text_with_ocr(page) -> str:
    #this function uses OCR to extract text from a PDF page when the text extraction fails (aka the page is an image or has no text).
    pix = page.get_pixmap(dpi=300)
    image = Image.open(io.BytesIO(pix.tobytes("png")))
    text = pytesseract.image_to_string(image, lang="eng")
    return text.strip()

def extract_text_from_pdf(path: str) -> str:
    #this function extracts text from a PDF file using PyMuPDF and OCR as a fallback if necessary.
    doc = fitz.open(path)
    all_text = []

    for page in doc:
        text = page.get_text()
        if text.strip():
            all_text.append(text)
        else:
            ocr_text = extract_text_with_ocr(page)
            all_text.append(ocr_text)

    return "\n".join(all_text).strip()
