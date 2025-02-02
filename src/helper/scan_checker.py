from fastapi.exceptions import HTTPException
from typing import Tuple
from .enums import ScanEnums
import fitz 


class ScanChecker:
    
    @staticmethod
    async def is_scan(file_path: str) -> Tuple[bool, str]:
        
        try:
            doc = fitz.open(file_path)
            text_pages = sum(1 for page in doc if page.get_text().strip())  
            
            if text_pages == len(doc) :
                return (False, ScanEnums.NATIVE_PDF.value)  
            
            return (True, ScanEnums.SCANNED_PDF.value)

        except Exception as e:
            raise HTTPException(500, f"PDF analysis failed: {str(e)}")
