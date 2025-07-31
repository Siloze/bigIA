from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
from ai import load_modele
import argparse
from llama_cpp import Llama

app = Flask(__name__)
CORS(app)

def generate_tokens(modele: Llama, full_prompt: str):
    # prompt = [
    #     {"role": "user", "content": full_prompt}
    # ]
    # output = modele.create_chat_completion(
    #     messages=prompt,
    #     max_tokens=512,
    #     stop=["</s>"],
    #     # seq
    # )
    for token in modele.create_completion(prompt=full_prompt, stream=True, max_tokens=512):
        text = token["choices"][0]["text"]
        print(text, end="", flush=True)
        yield f"data: {text}\n\n"

    #set CMAKE_ARGS=-DGGML_CUDA=ON -DLLAMA_KV_CACHE_UNIFIED=0

@app.route("/", methods=["GET"])
def generate_response():
    prompt = request.args.get("prompt")
    print(prompt)
    if (prompt):
        return Response(stream_with_context(generate_tokens(modele, prompt)), mimetype='text/event-stream')
    return "Error: prompt is not valid."

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", type=str, required=True)
    args = parser.parse_args()

    modele = load_modele(args.model_path)
    #modele = None
    app.run(host="0.0.0.0", port=6000)
