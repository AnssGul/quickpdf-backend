from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from app.services.pdf_split_service import split_pdf

router = APIRouter(prefix="/split", tags=["Split PDF"])

@router.post("/")
async def split(
    file: UploadFile = File(...),
    start_page: int = Form(...),
    end_page: int = Form(...)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    try:
        output_path = await split_pdf(file, start_page, end_page)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return FileResponse(
        path=output_path,
        filename=f"split_{file.filename}",
        media_type="application/pdf"
    )