import os
import faiss
import pickle
import numpy as np
from openai import OpenAI
from sentence_transformers import SentenceTransformer

# Initialize embedding model (OpenAI or fallback)
try:
    openai_client = OpenAI()
    use_openai = True
except:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    use_openai = False

INDEX_FILE = "mizan_faiss.index"
META_FILE = "mizan_metadata.pkl"

# --- Embedding Function ---
def embed_text(text):
    if use_openai:
        response = openai_client.embeddings.create(
            input=text,
            model="text-embedding-ada-002"
        )
        return np.array(response.data[0].embedding, dtype='float32')
    else:
        return np.array(model.encode(text), dtype='float32')

# --- Initialize or Load FAISS Index ---
def load_faiss():
    if os.path.exists(INDEX_FILE) and os.path.exists(META_FILE):
        index = faiss.read_index(INDEX_FILE)
        with open(META_FILE, "rb") as f:
            metadata = pickle.load(f)
        return index, metadata
    else:
        dim = 1536 if use_openai else 384
        index = faiss.IndexFlatL2(dim)
        metadata = []
        return index, metadata

# --- Save FAISS Index + Metadata ---
def save_faiss(index, metadata):
    faiss.write_index(index, INDEX_FILE)
    with open(META_FILE, "wb") as f:
        pickle.dump(metadata, f)

# --- Add Entry to Index ---
def add_to_index(text, metadata_item):
    vec = embed_text(text).reshape(1, -1)
    index, metadata = load_faiss()
    index.add(vec)
    metadata.append(metadata_item)
    save_faiss(index, metadata)

# --- Search Index ---
def search_similar_insights(text, top_k=3):
    vec = embed_text(text).reshape(1, -1)
    index, metadata = load_faiss()
    if index.ntotal == 0:
        return []
    D, I = index.search(vec, top_k)
    results = [metadata[i] for i in I[0] if i < len(metadata)]
    return results