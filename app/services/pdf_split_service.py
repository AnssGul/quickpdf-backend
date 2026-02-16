import os
import uuid
from PyPDF2 import PdfReader, PdfWriter
from fastapi import UploadFile

UPLOAD_DIR = "tmp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def split_pdf(file: UploadFile, start_page: int, end_page: int):
    """
    Splits a PDF from start_page to end_page (1-indexed inclusive)
    """
    # Save uploaded file
    input_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}.pdf")
    with open(input_path, "wb") as f:
        content = await file.read()
        f.write(content)

    reader = PdfReader(input_path)
    writer = PdfWriter()

    total_pages = len(reader.pages)
    if start_page < 1 or end_page > total_pages or start_page > end_page:
        raise ValueError("Invalid page range")

    # Add selected pages
    for i in range(start_page - 1, end_page):
        writer.add_page(reader.pages[i])

    output_path = os.path.join(UPLOAD_DIR, f"split_{uuid.uuid4()}.pdf")
    with open(output_path, "wb") as f:
        writer.write(f)

    return output_path