from flask import Flask, request, jsonify, render_template
from find_matching import initialize_model_and_data, find_similar_docs
import os
from pdf2txt import pdf2text  

app = Flask(__name__)

# Initialize model and data
folder_path = r'CourtCases_txt'
model, document_embeddings, file_names = initialize_model_and_data(folder_path)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/find_similar', methods=['POST'])
def find_similar():
    input_option = request.form.get('input_option')
    query = ""

    if input_option == 'Text Input':
        query = request.form.get('text_input')

    elif input_option == 'Upload PDF':
        uploaded_file = request.files.get('uploaded_pdf_file')
        if uploaded_file:
            # Save the uploaded file temporarily
            temp_pdf_path = "temp_uploaded_pdf.pdf"
            uploaded_file.save(temp_pdf_path)
            
            try:
                query = pdf2text(temp_pdf_path)
            except Exception as e:
                return jsonify({'error': f"An error occurred while extracting text from the PDF: {e}"}), 400

    # Number of documents to display
    num_docs = int(request.form.get('num_docs', 5))

    if not query:
        return jsonify({'error': "Please enter text or upload a PDF file to find similar cases."}), 400

    # Find similar documents
    similar_docs = find_similar_docs(query, model, document_embeddings, file_names, top_n=num_docs)

    results = []
    for doc, score in similar_docs:
        file_path = os.path.join(folder_path, doc)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            results.append({
                'doc': doc,
                'score': f"{score * 100:.2f}%",
                'content': content.splitlines()[:100]  # Preview only the first 100 lines
            })
        else:
            results.append({'doc': doc, 'score': f"{score * 100:.2f}%", 'error': "File does not exist."})

    return jsonify({'results': results})

if __name__ == "__main__":
    app.run(debug=True)