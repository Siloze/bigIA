FROM python:3.13-slim

# Dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Installer llama-cpp-python avec support CPU
RUN pip install --no-cache-dir llama-cpp-python
RUN pip install flask sentence_transformers faiss-cpu
RUN pip install requests langchain

# Créer dossier de travail
WORKDIR /app

# Entrée du conteneur
CMD ["python", "src/deamons.py", "--model_path", "./models/Mistral-7B-Instruct-v0.3-Q4_K_M.gguf"]
