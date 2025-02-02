import logging
from config import settings
from scraper import PDFScraper, GetFile
from helper import FileValidator
from scraper import PDFProcessor
from database import VectorDBManager

class ScrapeController:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.vdb_manager = VectorDBManager()
        self.should_scrape = self.vdb_manager.is_collection_empty()
        self.scraper = PDFScraper(settings.TARGET_WEBSITE)

    async def store_into_vdb(self):
        if not self.should_scrape:
            print("Database already populated. Skipping scraping.")
            return

        categories = self.scraper.get_main_categories()
        
        for category, category_url in categories:
            subcategories = self.scraper.get_subcategory_links(category_url)
            stored_count = 0
            
            for subcategory, sub_url, file_title in subcategories:
                if stored_count >= settings.MAX_PDFS_PER_CATEGORY:
                    break

                file_url, file_type, file_size  = self.scraper.find_pdf_link(sub_url)
                if not file_url and file_type and file_size:
                    continue
                
                isvalid, message = await FileValidator.isvalid(file_type, file_size)
                if not isvalid:
                    self.logger.error(f"Invalid file: {file_title} - {message}")
                    continue

                file_path = await GetFile().file_path(file_url, category, subcategory)

                # Process and store
                processor = PDFProcessor()
                document = await processor.process_pdf(file_path, file_title, sub_url, category, subcategory)
                if document:
                    VectorDBManager().store_document(document)
                    stored_count += 1
                