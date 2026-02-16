from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from typing import List
from app.services.merge_service import merge_pdfs

router = APIRouter(prefix="/merge", tags=["Merge PDF"])

@router.post("/")
async def merge(files: List[UploadFile] = File(...)):

    if len(files) < 2:
        raise HTTPException(status_code=400, detail="Upload at least 2 PDFs")

    for file in files:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files allowed")

    output_path = await merge_pdfs(files)

    return FileResponse(
        path=output_path,
        filename="merged.pdf",
        media_type="application/pdf"
    )