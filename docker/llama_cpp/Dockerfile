FROM nvidia/cuda:12.9.1-devel-ubuntu22.04

# Dépendances système
RUN apt-get update && apt-get install -y \
    python3.10 python3-pip build-essential cmake git curl \
    && rm -rf /var/lib/apt/lists/*

# Mettre Python par défaut
RUN ln -s /usr/bin/python3.10 /usr/bin/python

# Variables pour la compilation avec CUDA
ENV LLAMA_CUBLAS=1
ENV FORCE_CMAKE=1

# Installer llama-cpp-python avec support GPU
RUN pip install --no-cache-dir llama-cpp-python
RUN pip install flask sentence_transformers faiss-cpu
RUN pip install requests langchain

# Créer le dossier de travail
WORKDIR /app

# Entrée du conteneur
CMD ["python", "./src/deamons.py", "--modele_path ./models/Mistral-7B-Instruct-v0.3-Q4_K_M.gguf"]
