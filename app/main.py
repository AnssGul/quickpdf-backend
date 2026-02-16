from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import compress, merge, pdf_split, word_to_pdf

app = FastAPI(title="QuickPDF Pro API")

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace "*" with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(compress.router)
app.include_router(merge.router)
app.include_router(pdf_split.router)
app.include_router(word_to_pdf.router)

@app.get("/")
def root():
    return {"message": "QuickPDF Pro API Running 🚀"}