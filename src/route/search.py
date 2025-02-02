from fastapi import APIRouter, File, UploadFile, HTTPException
from helper import ScanChecker
from helper import GetText
from database import VectorDBManager
import os
import tempfile


search_router = APIRouter()

@search_router.post("/search")
async def search(file: UploadFile = File(...)):

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDFs are allowed.")
    if file.size > 3 * 1024 * 1024: 
        raise HTTPException(status_code=400, detail="File size exceeds the allowed limit of 3MB.")
    
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    is_scanned, _ = await ScanChecker.is_scan(tmp_path)
    
    if is_scanned:
        text = await GetText.get_scannedpdf_text(tmp_path)
    else:
        text = await GetText.get_nativepdf_text(tmp_path)
    
    # Cleanup
    os.unlink(tmp_path)
    
    results = VectorDBManager().search_documents(text)
    return {"matches": results}    