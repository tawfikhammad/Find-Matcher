import PyPDF2
import sys

def pdf2text(pdf_path):

    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() or ""
    except Exception as e:
        return f"An error occurred: {e}"
    return text

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pdf2txt.py <pdf_file_path>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    extracted_text = pdf2text(pdf_path)
    print(extracted_text)
