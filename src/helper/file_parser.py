import pymupdf
from pdf2image import convert_from_path
import asyncio
from config import settings
import pytesseract
pytesseract.pytesseract.tesseract_cmd =  settings.TESSERACT_CMD

class FileParser:
    
    @staticmethod
    async def get_nativepdf_text(file_path) -> str:
        doc = pymupdf.open(file_path)
        text = "".join(page.get_text() for page in doc)
        return text

    @staticmethod
    async def get_scannedpdf_text(file_path: str) -> str:
        images = await asyncio.to_thread(
            convert_from_path,
            file_path,
            dpi=300,
            fmt="jpeg",
            thread_count=4,
            grayscale=True)

        # Extract text from each image asynchronously
        text_list = []
        for img in images:
            page_text = await asyncio.to_thread(pytesseract.image_to_string, img, lang="ara")
            if page_text.strip():
                text_list.append(page_text.strip())

        extracted_text = "\n\n".join(text_list)
        return extracted_text
