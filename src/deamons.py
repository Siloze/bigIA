from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import ai
from rag import RAG, get_data_from_dir
import argparse
from config import get_param, load_config, set_param
from history import append_to_history, clear_history, get_last_messages, get_all_messages
app = Flask(__name__)
CORS(app)
CONFIG_PATH="./config.ini"

@app.route("/response", methods=["POST"])
def generate_response():
    question = request.form.get("question", "")
    pre_prompt = request.form.get("pre_prompt", "")
    rag_prompt = request.form.get("rag_prompt", "")

    web_search = request.form.get("web_search", "false")
    use_rag = request.form.get("use_rag", "")
    fichier = request.files.get("fichier")

    set_param(CONFIG_PATH, "prompting", "pre_prompt", pre_prompt)
    set_param(CONFIG_PATH, "prompting", "rag_prompt", rag_prompt)

    if fichier and fichier.filename != "":
        contenu = fichier.read().decode("utf-8")
        answer = ai.generate_response_file(contenu, fichier.filename, modele, question, pre_prompt)
    elif web_search == "true":
        answer = ai.generate_response_web(modele, question, pre_prompt, rag)
    elif use_rag == "false":
        answer = ai.generate_response(modele, question, pre_prompt= pre_prompt)
    else:
        answer = ai.generate_response(modele, question, pre_prompt= pre_prompt, rag= rag, rag_prompt= rag_prompt)
    append_to_history(question, answer)
    return jsonify({"answer": answer})

@app.route("/history", methods=["GET"])
def history():
    history = []
    if request.method == "GET":
        history = get_all_messages()
    return history

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

    data = get_data_from_dir(args.rag_data)
    rag = RAG(data, modele_path=args.rag_path)
    modele = ai.load_modele(args.model_path)

    app.run(host="0.0.0.0", port=5000)
