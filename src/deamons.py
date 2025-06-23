from flask import Flask, render_template, request, jsonify
import ai
from rag import RAG
import argparse

print("name: ", __name__)
app = Flask(__name__)

@app.route("/response", methods=["POST"])
def generate_response():
    if request.method == "POST":
        data = request.json
        question = data.get("question", "")
        pre_prompt = data.get("pre_prompt", "")
        answer = ai.generate_response(pre_prompt, question, modele, rag)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--modele_path", type=str, required=True)
    parser.add_argument("--rag_path", type=str, default="sentence-transformers/all-MiniLM-L6-v2")
    parser.add_argument("--rag_data", type=str, default="./data/")
    args = parser.parse_args()

    rag = RAG(args.rag_path, args.rag_data)
    modele = ai.load_modele(args.modele_path)

    app.run(host="0.0.0.0", port=5000)
