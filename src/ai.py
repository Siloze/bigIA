from llama_cpp import Llama
from rag import RAG
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
def load_modele(path):
    llm = Llama(
        model_path=path,
        n_ctx=4096,  # contexte (augmente si tu veux du RAG plus tard)
        n_threads=8,  # nombre de threads CPU (ajuste selon ta machine)
    )
    return llm

def generate_response(question: str, modele: Llama, rag: RAG):
    pre_prompt = (
        "Tu es un assistant intelligent. Tu disposes parfois d'informations complémentaires extraites de documents. "
        "Si une question est clairement en lien avec ces informations, utilise-les. "
        "Sinon, ignore-les complètement et réponds uniquement en te basant sur tes propres connaissances générales. "
        "Tu es capable de répondre à de nombreuses questions de culture générale. "
        "Ne fais jamais référence au fait qu'il y a des documents ou du contexte sauf si la question le mentionne."
    )

 # Nombre de chunks à récupérer
    k = 5

    # Boucle d'interaction
    if question.strip().lower() in ["exit", "quit"]:
        print("Fin du programme.")
        return

    # Encoder la question
    question_embedding = rag.embedder.encode([question], convert_to_numpy=True)

    # Rechercher les k chunks les plus proches
    distances, indices = rag.index.search(question_embedding, k)

    # Récupérer les chunks correspondants
    retrieved = [(rag.chunks[i], rag.chunk_sources[i]) for i in indices[0]]

    # Construire le prompt complet avec contexte + question
    context = "\n\n---\n\n".join(f"[{src}]\n{txt}" for txt, src in retrieved)
    full_prompt = f"[INST] {pre_prompt}\n\n{context}\n\nQuestion:\n{question} [/INST]"

    print(f"Full prompt: {full_prompt}\n")
    output = modele(full_prompt, max_tokens=512, stop=["</s>"])

    response = output["choices"][0]["text"].strip()
    print(response)
    return response





   
