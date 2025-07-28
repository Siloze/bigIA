from rag import RAG, get_data_from_dir, encode_chunks
from history import DISCUSSIONS_PATH
import json
from sentence_transformers import SentenceTransformer
import faiss
from typing import List, TypedDict

def init_semantic_memory_faiss(rag_embedder: SentenceTransformer):
    discussions_data = get_data_from_dir(DISCUSSIONS_PATH)

    chuncks: List[str] = []
    for discussion_file in discussions_data:
        all_history = discussion_file["content"]
        all_history_json = json.loads(all_history)
        for echange in all_history_json:
            question = echange["question"]
            answer = echange["answer"]

            chuncks.append(f"{question}")
    memory_embeddings = encode_chunks(rag_embedder, chuncks)
    dimension = memory_embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(memory_embeddings)
    return index, chuncks
    


    
