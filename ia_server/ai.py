import os
os.environ["LLAMA_DEBUG"] = "1"

from llama_cpp import Llama
def token_callback(token: str):
    print(token, end="", flush=True)

def load_modele(path):
    llm = Llama(
        model_path=path,
        n_ctx=4096,           # Pour mistral 7B: 4096. 128000 / 16384 pour Nemo
        n_gpu_layers=-1,       # 0 si CPU only
        n_threads=4,
        verbose=True,
        seed=42,
        backend="metal"          # Force le backend Metal (GPU Apple)
    )
    return llm






   
