from sentence_transformers import SentenceTransformer
import faiss
import os
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter

class RAG_DATA:
    name: str
    content: str

def split_text_recursive(text, chunk_size=1000, overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = text_splitter.split_text(text)
    return chunks

def split_text_paragraphs(text, chunk_size=300, overlap=50):
    paragraphs = re.split(r'\n{2,}', text)
    chunks = []
    current_chunk = ""
    for para in paragraphs:
        if len(current_chunk) + len(para) < chunk_size:
            current_chunk += para + "\n\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = para + "\n\n"
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks


def split_text_sliding_window(text, chunk_size=300, overlap=50):
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    chunk = []

    total_length = 0
    i = 0
    while i < len(sentences):
        sentence = sentences[i]
        if total_length + len(sentence) <= chunk_size:
            chunk.append(sentence)
            total_length += len(sentence)
            i += 1
        else:
            chunks.append(" ".join(chunk).strip())
            # reculer pour l'overlap
            i = max(i - overlap // len(sentence), 0)
            chunk = []
            total_length = 0

    if chunk:
        chunks.append(" ".join(chunk).strip())
    return chunks

def encode_chunks(embedder: SentenceTransformer, chunks):
    return embedder.encode(chunks, convert_to_numpy=True)

def get_data_from_dir(data_dir):
    path = data_dir
    data = []
    for filename in os.listdir(path):
        if filename.endswith(".txt"):
            file_path = os.path.join(path, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                full_text = f.read()
                data.extend({'name': filename, 'content': full_text}) 
    return data

class RAG:
    
    def __init__(self, data, modele_path: str = None, embedder: SentenceTransformer = None):
        self.data = data
        self.modele_path = modele_path
        self.embedder = embedder

        if embedder is None and modele_path is None:
            raise ValueError("Rag init: you have to set a modele_path or pre-charged embedder for initialization")
        if embedder is None: # Pour copier un modele déjà chargé dans un RAG
            self.load_modele()
        self.init_chunks()
        self.init_embeddings()
        self.init_faiss()

    def load_modele(self):
        self.embedder = SentenceTransformer(self.modele_path)
        
    def init_chunks(self):
        chunks = []

        for full_text in self.data:
            chunks.extend(split_text_recursive(full_text))
        self.chunks = chunks

    def init_embeddings(self):
        self.embeddings = encode_chunks(self.embedder, self.chunks)
    
    def init_faiss(self):
        dimension = self.embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(self.embeddings)
        self.index = index

