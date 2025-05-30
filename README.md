# Legal Matcher

Legal Matcher is an application designed to scrape, process, and match documents from a legal website (Egyption website). It uses web scraping to collect PDF documents, processes them to extract text, and stores them in a vector database for efficient searching and matching.

---

## Application Structure

```
Legal Matcher/
├── src/
│   ├── main.py                 # FastAPI application
│   ├── config/
│   ├── controller/
│   ├── vector_db/
|   |   ├── providers/
│   ├── helper/
│   │   ├── enums/
│   ├── route/
│   ├── scrape/
```

---

## How to Use the App

### Prerequisites

1. **Python 3.9+**
2. **Environment Variables**: Create a `.env` file in the `src` directory based on `.env.example`.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/tawfikhammad/Find-Matcher.git
   cd legal-matcher
   ```
2. Install dependencies:
   ```bash
   pip install -r src/requirements.txt
   ```
3. Set up the `.env` file:
   - Add the path to the Tesseract executable:
     ```plaintext
     TESSERACT_CMD="C:/Program Files/Tesseract-OCR/tesseract.exe"
     ```
   - Configure other settings as needed (e.g., `MAX_FILE_SIZE`, `ALLOWED_FILE_TYPES`).

### Running the Application

1. **Run the Scraper**:

   - Execute the scraper to download and process PDFs:
     ```bash
     cd src
     python run_scraper.py
     ```
   - This will scrape PDFs from the target website, process them, and store them in the vector database.

2. **Run the FastAPI Server**:

   - Start the FastAPI server:
     ```bash
     python main.py
     ```

3. **Using the API**:
   - **Welcome Endpoint**:
     - Visit `http://0.0.0.0:8000/welcome` to see a welcome message.
   - **Search Endpoint**:
     - Upload a PDF file to search for matching documents:
       ```bash
       curl -X POST -F "file=@path/to/your/file.pdf" http://0.0.0.0:8000/matcher/search
       ```
     - The API will return a list of matching documents based on the content of the uploaded file.

---

## Limitations

- **Target Website Dependency**:
  The scraper is designed to work with a specific website (`manshurat.org`). Changes to the website's structure may break the scraper.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
