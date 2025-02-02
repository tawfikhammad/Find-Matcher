import aiohttp
from urllib.parse import quote
import os
import string
import random
import aiofiles
from config import settings

class GetFile:
    def __init__(self):
        self.session = aiohttp.ClientSession()

    def random_key(self, length: int = 5) -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def get_file_path(self, subcategory: str, category_dir: str) -> str:
        file_name = f"{subcategory}_{self.random_key()}.pdf"
        return os.path.join(category_dir, file_name)

    async def file_path(self, file_url: str, category: str, subcategory: str) -> str:
        try:
            encoded_url = quote(file_url, safe=':/?&=')
            
            category_dir = os.path.join(settings.SCRAPED_DIR, category, subcategory)
            os.makedirs(category_dir, exist_ok=True)

            file_path = self.get_file_path(subcategory, category_dir)
            
            # Download and save file
            async with self.session.get(encoded_url) as response:
                if response.status != 200:
                    raise Exception(f"Failed to download file: {response.status}")
                
                async with aiofiles.open(file_path, 'wb') as f:
                    async for chunk in response.content.iter_chunked(1024):
                        await f.write(chunk)
            
            return file_path
            
        except Exception as e:
            print(f"Error downloading file: {str(e)}")
            return None

    async def close(self):
        await self.session.close()