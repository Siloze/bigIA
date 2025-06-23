# API LLM et Serveur Web

Ce projet contient une API pour faire tourner un modèle de langage (LLM) et un serveur web séparé pour l'interface utilisateur.

## Architecture

- **API LLM** : Service backend qui gère les requêtes vers le modèle de langage
- **Serveur Web** : Interface frontend pour interagir avec l'API

## Prérequis

- Python 3.8+
- Les dépendances listées dans `requirements.txt`

## Installation

1. Clonez le repository
```bash
git clone https://github.com/Siloze/bigIA.git
cd bigIA
```

2. Installez les dépendances
```bash
pip install -r requirements.txt
```

## Structure du projet

```
.
├── src/
│   ├── deamons.py          # API LLM
│   └── web_server/
│       └── server.py       # Serveur web
├── modeles/                # Modèle LLM (modèle embeddings optionnel)
├── data/                   # Données pour RAG
└── README.md
```

## Utilisation

### 1. Lancement de l'API LLM

L'API LLM peut être lancée avec différentes configurations :

#### Configuration minimale
```bash
python .\src\deamons.py --modele_path .\modeles\Mistral-7B-Instruct-v0.3-Q4_K_M.gguf
```

#### Configuration avec un RAG local (Retrieval-Augmented Generation)
```bash
python .\src\deamons.py --modele_path .\modeles\Mistral-7B-Instruct-v0.3-Q4_K_M.gguf --rag_path .\modeles\all-MiniLM-L6-v2\
```

#### Paramètres disponibles

- `--modele_path` : **Obligatoire** - Chemin vers le modèle LLM (format .gguf)
- `--rag_path` : *Optionnel* - Chemin vers le modèle d'embeddings local pour RAG
- `--rag_data` : *Optionnel* - Chemin vers les données pour RAG

### 2. Lancement du serveur web

```bash
python .\src\web_server\server.py
```

## Exemples d'utilisation

### Exemple complet avec RAG
```bash
# Terminal 1 - Lancement de l'API LLM
python .\src\deamons.py --modele_path .\modeles\Mistral-7B-Instruct-v0.3-Q4_K_M.gguf --rag_path .\modeles\all-MiniLM-L6-v2\

# Terminal 2 - Lancement du serveur web
python .\src\web_server\server.py
```

### Exemple sans RAG local
```bash
# Terminal 1 - Lancement de l'API LLM
python .\src\deamons.py --modele_path .\modeles\Mistral-7B-Instruct-v0.3-Q4_K_M.gguf

# Terminal 2 - Lancement du serveur web
python .\src\web_server\server.py
```

## Configuration

### Modèles supportés

- Modèles au format GGUF (ex: Mistral-7B-Instruct-v0.3-Q4_K_M.gguf)
- Modèles d'embeddings pour RAG (ex: all-MiniLM-L6-v2)

### Ports par défaut

- API LLM : Vérifiez la configuration dans `deamons.py`
- Serveur web : Vérifiez la configuration dans `server.py`

## Développement

### Structure des services

1. **API LLM** (`src/deamons.py src/api.py src/rag.py`)
   - Charge et initialise le modèle de langage
   - Gère les requêtes d'inférence
   - Intègre RAG pour l'enrichissement des réponses

2. **Serveur Web** (`src/web_server/server.py`)
   - Interface utilisateur
   - Communique avec l'API LLM
   - Gère les sessions utilisateur

## Dépannage

### Problèmes courants

- **Modèle non trouvé** : Vérifiez que le chemin vers le modèle est correct
- **Mémoire insuffisante** : Assurez-vous d'avoir suffisamment de RAM pour le modèle choisi
- **Port déjà utilisé** : Vérifiez qu'aucun autre service n'utilise les ports configurés

## Contribution

1. Fork le projet
2. Créez une branche pour votre feature
3. Committez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

## Licence

On verra plus tard