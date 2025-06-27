FROM python:3.13-slim

# Dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Installer llama-cpp-python avec support CPU
RUN pip install flask
RUN pip install requests
# Créer dossier de travail
WORKDIR /app

# Entrée du conteneur
CMD ["python", "./src/web_server/server.py"]
