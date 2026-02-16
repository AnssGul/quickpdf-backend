from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from app.services.pdf_service import compress_pdf
import os

router = APIRouter(prefix="/compress", tags=["Compress PDF"])

@router.post("/")
async def compress(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    output_path = await compress_pdf(file)

    return FileResponse(
        path=output_path,
        filename="compressed_" + file.filename,
        media_type="application/pdf"
    )