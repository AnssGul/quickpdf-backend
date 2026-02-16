import os
import uuid
import pikepdf
from fastapi import UploadFile
from typing import List

UPLOAD_DIR = "tmp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def merge_pdfs(files: List[UploadFile]):

    output_path = os.path.join(UPLOAD_DIR, f"merged_{uuid.uuid4()}.pdf")

    pdf_list = []

    # Save uploaded files temporarily
    for file in files:
        input_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}.pdf")

        with open(input_path, "wb") as f:
            f.write(await file.read())

        pdf_list.append(input_path)

    # Merge PDFs
    merged_pdf = pikepdf.Pdf.new()

    for pdf_path in pdf_list:
        with pikepdf.open(pdf_path) as pdf:
            merged_pdf.pages.extend(pdf.pages)

    merged_pdf.save(output_path)

    return output_path