import logging
from config import settings
from scrape import PDFScraper
from helper import FileValidator, FileParser, GetFilePath
from .srcaped_data_controller import PDFProcessor
from vector_db import VDBProviderFactory
from vector_db.vdb_enums import VectorDBType

class ScrapeController:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.vdb_factory = VDBProviderFactory()
        self.vdb_provider = self.vdb_factory.create(provider=VectorDBType.CHROMA.value)
        self.vdb_provider.initialize_collection(
            collection_name="LegalDocuments",
        )
        self.should_scrape = self.vdb_provider.is_collection_empty()
        self.scraper = PDFScraper(settings.TARGET_WEBSITE)

    async def store_into_vdb(self):
        """Store scraped documents into vector database."""
        if not self.should_scrape:
            self.logger.info("Database already populated. Skipping scraping.")
            print("Database already populated. Skipping scraping.")
            return

        try:
            categories = self.scraper.get_main_categories()
            total_stored = 0
            
            for category, category_url in categories:
                subcategories = self.scraper.get_subcategory_links(category_url)
                stored_count = 0
                
                self.logger.info(f"Processing category: {category}")
                
                for subcategory, sub_url, file_title in subcategories:
                    if stored_count >= settings.MAX_PDFS_PER_CATEGORY:
                        self.logger.info(f"Reached max PDFs limit for category: {category}")
                        break

                    try:
                        # Find PDF link
                        file_url, file_type, file_size = self.scraper.find_pdf_link(sub_url)
                        if not file_url or not file_type or not file_size:
                            self.logger.warning(f"No valid PDF found for: {file_title}")
                            continue
                        
                        # Validate file
                        isvalid, message = await FileValidator.isvalid(file_type, file_size)
                        if not isvalid:
                            self.logger.error(f"Invalid file: {file_title} - {message}")
                            continue

                        # Get file path
                        file_path = await GetFilePath().file_path(file_url, category, subcategory)

                        # Process and store document
                        processor = PDFProcessor()
                        document = await processor.process_pdf(
                            file_path, file_title, sub_url, category, subcategory
                        )
                        
                        if document:
                            # Store using the factory-created VDB manager
                            self.vdb_provider.store_document(document)
                            stored_count += 1
                            
                            self.logger.info(
                                f"Stored document: {file_title} "
                                f"(Category: {category}, Subcategory: {subcategory})"
                            )
                        else:
                            self.logger.error(f"Failed to process PDF: {file_title}")
                            
                    except Exception as e:
                        self.logger.error(f"Error processing {file_title}: {str(e)}")
                        continue
                
                self.logger.info(f"Category '{category}' completed. Stored {stored_count} documents.")
            
            self.logger.info(f"Scraping completed. Total documents stored: {total_stored}")
            
        except Exception as e:
            self.logger.error(f"Error during scraping process: {str(e)}")
            raise
        finally:
            self.vdb_provider.close_connection()
