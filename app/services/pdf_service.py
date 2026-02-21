import os
import uuid
import fitz  # PyMuPDF
from fastapi import UploadFile, HTTPException

UPLOAD_DIR = "temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def compress_pdf(file: UploadFile):
    try:
        unique_id = str(uuid.uuid4())
        input_path = os.path.join(UPLOAD_DIR, f"{unique_id}_input.pdf")
        output_path = os.path.join(UPLOAD_DIR, f"{unique_id}_compressed.pdf")

        # Save file
        with open(input_path, "wb") as f:
            f.write(await file.read())

        doc = fitz.open(input_path)

        # Save with garbage collection + compression
        doc.save(
            output_path,
            garbage=4,
            deflate=True,
            clean=True
        )

        doc.close()
        os.remove(input_path)

        return output_path

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Compression failed: {str(e)}"
        )    





# import os
# import uuid
# import subprocess
# from fastapi import UploadFile, HTTPException

# UPLOAD_DIR = "temp"

# # ensure temp folder exists
# os.makedirs(UPLOAD_DIR, exist_ok=True)


# async def compress_pdf(file: UploadFile, level: str = "ebook") -> str:
#     """
#     Compress PDF using Ghostscript

#     level options:
#         screen  -> lowest quality, highest compression
#         ebook   -> medium quality (recommended)
#         printer -> high quality
#         prepress-> very high quality
#     """

#     # validate compression level
#     allowed_levels = ["screen", "ebook", "printer", "prepress"]
#     if level not in allowed_levels:
#         level = "ebook"

#     try:
#         # generate unique filenames
#         unique_id = str(uuid.uuid4())
#         input_path = os.path.join(UPLOAD_DIR, f"{unique_id}_input.pdf")
#         output_path = os.path.join(UPLOAD_DIR, f"{unique_id}_compressed.pdf")

#         # save uploaded file
#         with open(input_path, "wb") as f:
#             f.write(await file.read())

#         # ghostscript command
#         command = [
#     "gswin64c",  # Windows fix
#     "-sDEVICE=pdfwrite",
#     "-dCompatibilityLevel=1.4",
#     f"-dPDFSETTINGS=/{level}",
#     "-dNOPAUSE",
#     "-dQUIET",
#     "-dBATCH",
#     f"-sOutputFile={output_path}",
#     input_path,
# ]

#         result = subprocess.run(command, capture_output=True)

#         if result.returncode != 0:
#             raise HTTPException(
#                 status_code=500,
#                 detail="Error compressing PDF"
#             )

#         # optional: remove original file
#         if os.path.exists(input_path):
#             os.remove(input_path)

#         return output_path

#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Compression failed: {str(e)}"
#         )