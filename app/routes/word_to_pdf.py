from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from app.services.word_to_pdf_service import file_to_pdf
import os

router = APIRouter(
    prefix="/word-to-pdf",
    tags=["Word to PDF"]
)

@router.post("/convert", response_class=FileResponse)
async def convert_file(file: UploadFile = File(...)):
    """
    Convert uploaded Word (.docx) or image file to PDF and return as FileResponse.
    """
    try:
        output_path = await file_to_pdf(file)
        return FileResponse(
            path=output_path,
            filename=os.path.basename(file.filename.rsplit('.', 1)[0] + ".pdf"),
            media_type="application/pdf"
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")