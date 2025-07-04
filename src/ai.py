from llama_cpp import Llama
from rag import RAG, encode_chunks, split_text_recursive
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from web import web_search_and_extract
import faiss

def load_modele(path):
    llm = Llama(
        model_path=path,
        n_ctx=4096,           # Pour mistral 7B: 4096. 128000 / 16384 pour Nemo
        n_threads=6,          # selon ton CPU
        n_gpu_layers=-1,       # 0 si CPU only
        verbose=True,
        seed=42,
        backend="metal"          # Force le backend Metal (GPU Apple)
    )
    return llm

def generate_response_web(modele: Llama, question: str, pre_prompt: str, rag_class: RAG):
    docs = web_search_and_extract(question)
    data = []
    for doc in docs:
        doc_name = doc['url']
        doc_content = doc['content']
        data.extend(f"-----{doc_name}-----\n" + doc_content)

    web_rag = RAG(data, embedder= rag_class.embedder)

    web_rag_prompt="Tu as des informations trouvé sur des sites internet, utilises les seulement si elles permettent de t'aider a répondre à la question posée. Sinon, n'en fais pas usage et n'en fais pas mention."
    
    return generate_response(modele, question, pre_prompt, web_rag, web_rag_prompt)


def generate_response_file(file_str: str, filename: str, modele: Llama, question: str, pre_prompt: str, rag: RAG = None, rag_prompt: str = ""):
    pre_prompt = pre_prompt + "\n\nVoici le contenue du fichier attaché à la demande, lis le et traite la question par rapport au contenue:\n" + filename + "\n" + file_str
    return generate_response(modele, question, pre_prompt, rag, rag_prompt)

def generate_response(modele: Llama, question: str, pre_prompt = "", rag: RAG = None, rag_prompt = ""):

    print(f"rag_prompt: {rag_prompt}")
    k = 1

    if question.strip().lower() in ["exit", "quit"]:
        print("Fin du programme.")
        return

    if rag is not None:
        question_embedding = rag.embedder.encode([question], convert_to_numpy=True)
        distances, indices = rag.index.search(question_embedding, k)
        retrieved = [(rag.chunks[i]) for i in indices[0]]

        context = "\n\n---\n\n".join(txt for txt in retrieved)
        full_prompt = f"[INST] {pre_prompt}\n\n{rag_prompt}\n{context}\n\nVoici la question:\n{question} [/INST]"
    else:
        full_prompt = f"[INST] {pre_prompt}\n\nVoici la question:\n{question} [/INST]"
    print(f"Full prompt: {full_prompt}\n")
    output = modele(full_prompt, max_tokens=512, stop=["</s>"])

    response = output["choices"][0]["text"].strip()
    print(response)
    return response





   
