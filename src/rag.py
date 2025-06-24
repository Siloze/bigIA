from sentence_transformers import SentenceTransformer
import faiss
import os
import re

# Fonction simple de découpage du texte en chunks avec chevauchement
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

class RAG:
    def __init__(self, modele_path, data_dir):
        self.modele_path = modele_path
        self.data_dir = data_dir
        self.load_modele(modele_path)
        self.load_chunks()
        self.encode_chunks()
        self.init_faiss()

    def load_modele(self, path):
        self.modele_path = path
        self.embedder = SentenceTransformer(path)
        
    def load_chunks(self):
        chunks = []
        chunk_sources = [] # A voir comment le retourner
        path = self.data_dir
        for filename in os.listdir(path):
            if filename.endswith(".txt"):
                file_path = os.path.join(path, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    full_text = f.read()
                    file_chunks = split_text_paragraphs(full_text, chunk_size=300, overlap=50)
                    chunks.extend(file_chunks)  # Ajoute les chunks à la liste globale
                    chunk_sources.extend([filename] * len(file_chunks))  # associer les sources
        self.chunks = chunks
        self.chunk_sources = chunk_sources
    
    def encode_chunks(self):
        self.embeddings = self.embedder.encode(self.chunks, convert_to_numpy=True)
    
    def init_faiss(self):
        dimension = self.embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(self.embeddings)
        self.index = index

