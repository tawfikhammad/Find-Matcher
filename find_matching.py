from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os
import warnings
warnings.simplefilter('ignore')

def initialize_model_and_data(folder_path):
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    documents = []
    file_names = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):  
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                documents.append(content)
                file_names.append(filename)

    document_embeddings = model.encode(documents)
    return model, document_embeddings, file_names

def find_similar_docs(query, model, document_embeddings, file_names, top_n=5):
    query_embedding = model.encode([query])
    cosine_similarities = cosine_similarity(query_embedding, document_embeddings).flatten()
    most_similar_indices = cosine_similarities.argsort()[-top_n:][::-1]
    most_similar_docs = [(file_names[idx], cosine_similarities[idx]) for idx in most_similar_indices]
    
    return most_similar_docs
