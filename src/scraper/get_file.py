import requests
from config import settings
import os
import string
import random
import aiofiles

class GetFile:

    def random_key(self, length: int=5):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def get_file_path(self, subcategory, category_dir):
        file_name = f"{subcategory}_{self.random_key(5)}"
        file_path = os.path.join(category_dir, file_name)
        return file_path

    async def file_path(self, file_url: str, category: str, subcategory: str) -> str:
        response = requests.get(file_url, stream=True)

        category_dir = os.path.join(settings.SCRAPED_DIR, category, subcategory)
        os.makedirs(category_dir, exist_ok=True)

        file_path = self.get_file_path(self, subcategory, category_dir)

        if os.path.exists(file_path):
            return self.get_file_path(self, subcategory, category_dir)

        async with aiofiles.open(file_path, 'wb') as f:
                    while chunk := await response.content.read(1028):
                        await f.write(chunk)

        return file_path
