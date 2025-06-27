from flask import Flask, render_template, request, jsonify
import ai
from rag import RAG
import argparse
from config import get_param, load_config, set_param

app = Flask(__name__)

CONFIG_PATH="./config.ini"

@app.route("/response", methods=["POST"])
def generate_response():
    question = request.form.get("question", "")
    pre_prompt = request.form.get("pre_prompt", "")
    rag_prompt = request.form.get("rag_prompt", "")
    fichier = request.files.get("fichier")

    set_param(CONFIG_PATH, "prompting", "pre_prompt", pre_prompt)
    set_param(CONFIG_PATH, "prompting", "rag_prompt", rag_prompt)

    if fichier and fichier.filename != "":
        contenu = fichier.read().decode("utf-8")
        answer = ai.generate_response_file(contenu, rag_prompt, pre_prompt, question, modele, rag)
    else:
        answer = ai.generate_response(rag_prompt, pre_prompt, question, modele, rag)

    return jsonify({"answer": answer})

@app.route("/config", methods=["GET", "POST"])
def config():
    if request.method == "GET":
        section = request.args.get("section")
        key = request.args.get("key")
        if not section or not key:
            return jsonify({"error": "Paramètres 'section' et 'key' requis en GET"}), 400

        value = get_param(CONFIG_PATH, section, key)
        if value is None:
            return jsonify({"error": "Paramètre non trouvé"}), 404
        return jsonify({"section": section, "key": key, "value": value})

    elif request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Corps JSON requis"}), 400

        section = data.get("section")
        key = data.get("key")
        value = data.get("value")

        if not section or not key or value is None:
            return jsonify({"error": "Les champs 'section', 'key' et 'value' sont requis"}), 400

        set_param(CONFIG_PATH, section, key, value)
        return jsonify({"message": "Paramètre mis à jour", "section": section, "key": key, "value": value})

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", type=str, required=True)
    parser.add_argument("--rag_path", type=str, default="sentence-transformers/all-MiniLM-L6-v2")
    parser.add_argument("--rag_data", type=str, default="./data/")
    args = parser.parse_args()

    rag = RAG(args.rag_path, args.rag_data)
    modele = ai.load_modele(args.model_path)

    app.run(host="0.0.0.0", port=5000)
