import streamlit as st
from find_matching import initialize_model_and_data, find_similar_docs
import os
from pdf2txt import pdf2text  

# Initialize model and data
folder_path = r'CourtCases_txt'
model, document_embeddings, file_names = initialize_model_and_data(folder_path)

st.title("Legal Document Similarity Finder")

# Sidebar to choose the input method (PDF or Text)
st.sidebar.title("Choose Input Method")
input_option = st.sidebar.radio("Select Input Type:", ('Text Input', 'Upload PDF'))

query = ""

if input_option == 'Text Input':
    query = st.text_area("Enter the text:")

if input_option == 'Upload PDF':
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    if uploaded_file is not None:
        # Save the uploaded file temporarily
        temp_pdf_path = "temp_uploaded_pdf.pdf"
        with open(temp_pdf_path, "wb") as f:
            f.write(uploaded_file.read())
        
        try:
            query = pdf2text(temp_pdf_path)
            st.success("Successfully extracted text from the uploaded PDF file.")
        except Exception as e:
            st.error(f"An error occurred while extracting text from the PDF: {e}")

# Number of documents to display
num_docs = st.sidebar.number_input("Number of similar documents:", min_value=1, max_value=10, value=5)

# Display results
if st.button("Find Similar Documents"):
    if not query:
        st.error("Please enter text or upload a PDF file to find similar cases.")
    else:
        # Find similar documents
        similar_docs = find_similar_docs(query, model, document_embeddings, file_names, top_n=num_docs)

        st.write(f"Top {num_docs} similar documents:")

        for doc, score in similar_docs:
            st.write(f"**{doc}** : {score*100:.2f}%")
            
            file_path = os.path.join(folder_path, doc)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # Split the content into lines
                lines = content.split('\n')
                if len(lines) > 100:
                    # Show only the first 100 lines by default
                    preview_content = "\n".join(lines[:100])
                    st.text_area(f"Preview of {doc}", preview_content, height=300)
                    
                else:
                    # Show the full content if it's less than 100 lines
                    st.text_area(f"Content of {doc}", content, height=300)
            else:
                st.error(f"File {doc} does not exist.")
