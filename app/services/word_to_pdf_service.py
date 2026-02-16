import os
import uuid
from fastapi import UploadFile, HTTPException
from docx2pdf import convert
from PIL import Image

UPLOAD_DIR = "tmp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def file_to_pdf(file: UploadFile) -> str:
    """
    Converts an uploaded Word DOCX file or image to PDF
    """
    filename = file.filename.lower()
    content = await file.read()

    # Save original file
    input_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{file.filename}")
    with open(input_path, "wb") as f:
        f.write(content)

    # Output PDF path
    output_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}.pdf")

    if filename.endswith(".docx"):
        # Convert Word to PDF
        convert(input_path, output_path)
    elif filename.endswith((".jpg", ".jpeg", ".png")):
        # Convert Image to PDF
        img = Image.open(input_path)
        if img.mode in ("RGBA", "LA"):
            img = img.convert("RGB")  # PDF does not support alpha
        img.save(output_path, "PDF", resolution=100.0)
    else:
        raise HTTPException(status_code=400, detail="Only DOCX and image files are supported")

    return output_path