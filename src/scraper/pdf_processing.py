import os
import logging
from typing import Optional
from helper import ScanChecker, GetText

class PDFProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @classmethod
    async def process_pdf(self, file_path: str, file_title: str, sub_url: str, category: str, subcategory: str) -> Optional[dict]:
        try:
            scan, message = ScanChecker.is_scan(file_path)
            if scan:
                os.remove(file_path)
                return None

            else: 
                text = GetText.get_nativepdf_text(file_path)
                pdf_filename = os.path.basename(file_path)

                return {
                    "pdf_filename": pdf_filename,
                    "content": text,
                    "metadata": {
                        "source": sub_url,
                        "title": file_title,
                        "category": category,
                        "subcategory": subcategory
                    }
                }

        except Exception as e:
            self.logger.error(f"Error processing PDF {sub_url}: {str(e)}")
            return None