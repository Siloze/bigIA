from llama_cpp import Llama


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

def generate_response(modele: Llama, full_prompt: str):
    output = modele(full_prompt, max_tokens=512, stop=["</s>"])
    response = output["choices"][0]["text"].strip()
    print(response)
    return response





   
