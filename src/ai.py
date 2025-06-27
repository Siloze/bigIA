from llama_cpp import Llama
from rag import RAG
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
def load_modele(path):
    llm = Llama(
        model_path=path,
        n_ctx=16384,           # Pour mistral 7B: 4096. 128000 pour Nemo
        n_threads=8,          # selon ton CPU
        n_gpu_layers=0,       # 0 si CPU only
        verbose=True,
        seed=42
    )
    return llm

def generate_response_file(str, rag_prompt, pre_prompt, question: str, modele: Llama, rag: RAG):
    pre_prompt = pre_prompt + "Voici le contenue du fichier attaché à la demande, lis le et traite la question par rapport au contenue:\nFichier.txt: " + str
    return generate_response(rag_prompt, pre_prompt, question, modele, rag)

def generate_response(rag_prompt, pre_prompt, question: str, modele: Llama, rag: RAG):

    k = 10

    if question.strip().lower() in ["exit", "quit"]:
        print("Fin du programme.")
        return

    question_embedding = rag.embedder.encode([question], convert_to_numpy=True)
    distances, indices = rag.index.search(question_embedding, k)
    retrieved = [(rag.chunks[i], rag.chunk_sources[i]) for i in indices[0]]

    context = "\n\n---\n\n".join(f"[{src}]\n{txt}" for txt, src in retrieved)
    full_prompt = f"[INST] {pre_prompt}\n\n{rag_prompt}\n{context}\n\nVoici la question:\n{question} [/INST]"
    #full_prompt = f"[INST] {pre_prompt}\n\nVoici la question:\n{question} [/INST]"
    print(f"Full prompt: {full_prompt}\n")
    output = modele(full_prompt, max_tokens=512, stop=["</s>"])

    response = output["choices"][0]["text"].strip()
    print(response)
    return response





   
