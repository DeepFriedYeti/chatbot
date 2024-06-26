import os
import PyPDF2
from sentence_transformers import SentenceTransformer
import faiss
import joblib
import nltk
nltk.download('punkt')

def extract_text_from_pdf(pdf_path):
    pdf_reader = PyPDF2.PdfReader(pdf_path)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        new_text = page.extract_text()
        text += new_text
    return text

def generate_embeddings(text, model_name='all-MiniLM-L6-v2'):
    model = SentenceTransformer(model_name)
    sentences = nltk.sent_tokenize(text)
    embeddings = model.encode(sentences)
    return sentences, embeddings, model

def create_vector_store(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

def save_vector_store(index, sentences, embeddings_file='embeddings.joblib', index_file='index.faiss'):
    joblib.dump(sentences, embeddings_file)
    faiss.write_index(index, index_file)

def load_vector_store(embeddings_file='embeddings.joblib', index_file='index.faiss'):
    sentences = joblib.load(embeddings_file)
    index = faiss.read_index(index_file)
    return sentences, index

def query_vector_store(index, sentences, model, query, top_k=5):
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, top_k)
    distances[0]=distances[0][::-1]
    print(distances)
    indices[0]=indices[0][::-1]
    results = [sentences[i] for i in indices[0]]
    return results

def handle_query(query, embeddings_file='embeddings.joblib', index_file='index.faiss', model_name='all-MiniLM-L6-v2'):
    pdf_path = 'FS-Rules_2024_v1.1-2.pdf'
    if os.path.exists(embeddings_file) and os.path.exists(index_file):
        # Load existing embeddings and index
        sentences, index = load_vector_store(embeddings_file, index_file)
        model = SentenceTransformer(model_name)
    else:
        # Generate embeddings and create index
        text = extract_text_from_pdf(pdf_path)
        sentences, embeddings, model = generate_embeddings(text, model_name)
        index = create_vector_store(embeddings)
        save_vector_store(index, sentences, embeddings_file, index_file)

    # Query the vector store
    results = query_vector_store(index, sentences, model, query)
    return results
