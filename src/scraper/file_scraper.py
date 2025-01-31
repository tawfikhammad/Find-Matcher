from fastapi import status
from bs4 import BeautifulSoup
from typing import List, Tuple
from urllib.parse import urljoin
import requests
from..config import settings

class PDFScraper:
    def __init__(self, base_url = settings.TARGET_WEBSITE):
        self.url = base_url


    def get_main_categories(self) -> List[Tuple[str, str]]:
        response = requests.get(self.base_url)

        if response.status_code != status.HTTP_200_OK:
            raise Exception(f"Failed to fetch main page: {response.status_code}")

        soup = BeautifulSoup(response.content, "html.parser")
        dropdown = soup.find("li", class_="dropdown")
        
        categories = []
        if dropdown:
            submenu = dropdown.find("ul", class_="dropdown-menu multi-level")
            for item in submenu.find_all("li", class_="dropdown-submenu"):
                title = item.a.text.strip()
                link = urljoin(self.base_url, item.a["href"])
                categories.append((title, link))
        
        return categories
    

    def get_subcategory_links(self, category_url: str) -> List[Tuple[str, str]]:
        response = requests.get(category_url)
        soup = BeautifulSoup(response.content, "html.parser")
        subcategories = []
        
        for sub in soup.find_all("h2"):
            file_title = sub.a.text.strip()
            sub_link = urljoin(self.base_url, sub.a["href"])

            sub_info_div = sub.find_next("div", class_="inline-info") 
            sub_title_tag = sub_info_div.find("span", class_="lineage-item lineage-item-level-0") 
            sub_title = sub_title_tag.text.strip()
            subcategories.append((sub_title, sub_link, file_title))
        
        return subcategories
    
    
    def find_pdf_link(self, page_url: str) -> Tuple[str, str, int]:
        response = requests.get(page_url)
        soup = BeautifulSoup(response.content, "html.parser")

        file_link_tag = soup.find("a", href=True, text="Download")

        if file_link_tag:
            file_url = urljoin(self.base_url, file_link_tag["href"])
            file_attr = file_link_tag['type'].split(';')

            file_type = file_attr[0]
            file_size = int(file_attr[1].split('=')[1])

            return file_url, file_type, file_size
        return None