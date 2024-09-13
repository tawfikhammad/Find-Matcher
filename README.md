# Find Similar Cases

This project provides a tool to find similar legal documents by comparing text extracted from uploaded PDFs or user input.

## Content

1. [Overview](#overview)
2. [How the Code Works](#how-the-code-works)
3. [Dataset](#dataset)
4. [Interact with API](#interact-with-api)
5. [Watch the Demo](#watch-the-demo)
----

## Overview

The application is designed to identify related legal documents from a given query, whether it be entered manually as text or extracted from an uploaded PDF. The user can choose the number of similar issues and read their content.

It consists of three main components:

1. **PDF to Text Conversion**: Extracts text content from PDF files.
2. **Document Similarity Search**: Finds the top similar documents using `sentence embeddings` and `cosine similarity`.
3. **Streamlit Web Interface**: An interactive UI to input queries and view results.


## How the Code Works

1. **`pdf2txt.py`**:

This file handles the conversion of PDF files to text using `PyPDF2` module

It Contains `pdf2text` function: 

   - pdf2text(pdf_path): Reads the PDF file from the specified path and extracts text from each page and returns the extracted text.


2. **`find_matching.py`**:

This file finds similar documents and initializes the model and data.

It contains two main functions:

   - `initialize_model_and_data(folder_path)`: Loads a pre-trained SentenceTransformer model **all-MiniLM-L6-v2** and encodes documents from the specified folder.

    The function takes the path to the folder containing text files. 
    It returns the model, the embeddings for the documents and a list of file names.


  - `find_similar_docs(query, model, document_embeddings, file_names, top_n=5)`: Finds and ranks similar documents based on a given query using **cosine similarity**.

    It takes the following as inputs:
    * **query**: The query text to be compared.
    * **model**: The SentenceTransformer model used for encoding.
    * **document_embeddings**: The precomputed embeddings of the documents.
    * **file_names**: The list of document file names.
    * **top_n**: The number of top similar documents to return (default is 5).

    It returns a list of tuples where each tuple contains a file name and its similarity score.

3. **`app.py`**:
This file provides a web interface using **Streamlit**: Allows users to either enter text manually or upload a PDF file and then shows the top similar documents along with their content and similarity scores..

* If a PDF is uploaded, the text is extracted using `pdf2text` and then compared to the document embeddings.
* If he enters text manually, The text compared to the document embeddings directly.


4. **`requirements.txt`**:
   - Lists the necessary Python packages.

------

## Dataset:

There are many cases about  FAMILY LAW IN AUSTRALIA with `.pdf` extention.

honestly i get data in `.txt` extention but I use a small python script to convert from `.txt` to `.pdf`.

**NOTE** **The data is about FAMILY LAW IN AUSTRALIA. Once i find the Egyption data related to legal courts, it is easy to use it.**

----

## Interact with API:
I Build a treamlit app and connect it with Streamlit cloud to can be interacted with others.

### Access the App from this link: https://find-matching-cases.streamlit.app/

LET'S interact with app:

Feel free to use any docu from [CourtCases_pdf]() or put the text manually and the app will show the most similar documents, their similarity scores, and a preview of their content.

Note: Users can adjust the number of similar documents.

----

## Watch the Demo

[DEMO](https://github.com/user-attachments/assets/bab000cb-c7cc-4eb0-bc36-8d47bc049b75)
