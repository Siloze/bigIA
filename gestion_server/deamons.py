from flask import Flask, Response, request, stream_with_context, jsonify
from flask_cors import CORS
import prompt
from rag import RAG, get_data_from_dir
import argparse
from config import load_config, set_param, get_param_from_config, get_param_from_file
from history import append_to_history, get_discussion, get_all_messages, get_all_discussions, add_new_discussion, delete_discussion, rename_discussion
import requests

app = Flask(__name__)
CORS(app)
CONFIG_PATH="./config.ini"
AI_API_URL="http://88.187.95.147:6000"
# AI_API_URL="http://localhost:6000"
rag: RAG

def send_prompt(full_prompt: str, question: str, chat_id: int):
    params = {"prompt": full_prompt}
    print(full_prompt)
    full_response = "réponse de merde"
    with requests.get(AI_API_URL, params=params, stream=True) as response:
        if response.status_code == 200:
            for line in response.iter_lines(decode_unicode=True):
                if line and line.startswith("data: "):
                    token = line.removeprefix("data: ")
                    full_response += token
                    print(token, end="", flush=True)
                    yield f"data: {token}\n\n"
        else:
            yield f"data: [ERREUR {response.status_code}]\n\n"
        append_to_history(chat_id, question, full_response)

        yield "data: [DONE]\n\n"


@app.route("/response", methods=["GET"])
def generate_response():
    pre_prompt = request.args.get("pre_prompt", "")
    question = request.args.get("question", "")
    web_search = request.args.get("web_search", "false")
    chat_id = int(request.args.get("id", 0))

    fichier = None


    set_param(CONFIG_PATH, "prompting", "pre_prompt", pre_prompt)

    config = load_config(CONFIG_PATH)

    rag_prompt =  get_param_from_config(config, "prompting", "rag_prompt", "")
    semantic_memory_prompt =  get_param_from_config(config, "prompting", "semantic_memory_prompt", "")
    direct_memory_prompt =  get_param_from_config(config, "prompting", "direct_memory_prompt", "")

    rag_count = int(get_param_from_config(config, "rag", "rag_count", "0"))
    semantic_memory_count = int(get_param_from_config(config, "memory", "semantic_memory_count", "0"))
    direct_memory_count = int(get_param_from_config(config, "memory", "direct_memory_count", "0"))


    full_prompt = pre_prompt
    if fichier and fichier.filename != "":
        contenu = fichier.read().decode("utf-8")
        full_prompt = f"{full_prompt}\n{prompt.generate_prompt_file(contenu, fichier.filename)}"
    if web_search == "true":
        full_prompt = f"{full_prompt}\n{prompt.generate_prompt_web(question, rag)}"
    if rag_count > 0:
        full_prompt = f"{full_prompt}\n{prompt.generate_rag_prompt(question, rag, rag_prompt, rag_count)}"
    if direct_memory_count > 0:
        full_prompt = f"{full_prompt}\n{prompt.generate_direct_memory_prompt(direct_memory_prompt, direct_memory_count, chat_id)}"
    if semantic_memory_count > 0:
        full_prompt = f"{full_prompt}\n{prompt.generate_semantic_memory_prompt(question, rag, semantic_memory_prompt, semantic_memory_count)}"
    final_prompt = prompt.generate_final_prompt(full_prompt, question);
    return Response(stream_with_context(send_prompt(final_prompt, question, chat_id)),
                        content_type='text/event-stream')
    # return jsonify({"answer": answer})

@app.route("/all_discussions", methods=["GET", "POST"])
def all_discussions():
    discussions = []
    if request.method == "GET":
        discussions = get_all_discussions()
    if request.method == "POST":
        discussions = add_new_discussion("Discussion")
    return discussions

@app.route("/discussion", methods=["GET"])
def discussion():
    discussions = []
    if request.method == "GET":
        id = request.args.get("id")
        print("id:")
        print(id)
        id = int(id);
        discussions = get_discussion(id)
    return discussions


@app.route('/discussion/<int:id>', methods=['DELETE'])
def delete_discu(id):
    delete_discussion(id)
    return jsonify({"message": f"Discussion {id} deleted."}), 200

@app.route('/discussion/<int:id>', methods=['PUT'])
def raname_discussion(id):
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Missing 'name' in request body"}), 400
    rename_discussion(id, data["name"])
    return jsonify({"message": f"Discussion {id} renamed to '{data['name']}'"}), 200

@app.route("/history", methods=["GET"])
def history():
    history = []
    if request.method == "GET":
        id = request.args.get("id")
        id = int(id);
        history = get_all_messages(id)
    return history

@app.route("/rag/reload", methods=["POST"])
def reset_rag():
    global rag
    config = load_config(CONFIG_PATH)
    rag_data_path = get_param_from_config(config, "rag", "data_path", "./data/")
    print(f"New rag path: {rag_data_path}\n")
    data = get_data_from_dir(rag_data_path)
    print("loading rag with datas\n")
    rag = RAG(data, embedder= rag.embedder)
    print("Rag load completed !\n")
    return 200

@app.route("/config", methods=["GET", "POST"])
def config():
    if request.method == "GET":
        section = request.args.get("section")
        key = request.args.get("key")
        if not section or not key:
            return jsonify({"error": "Paramètres 'section' et 'key' requis en GET"}), 400


        value = get_param_from_file(CONFIG_PATH, section, key, "")
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
    parser.add_argument("--rag_path", type=str, default="sentence-transformers/all-MiniLM-L6-v2")
    args = parser.parse_args()

    config = load_config(CONFIG_PATH)
    rag_data_path = get_param_from_config(config, "rag", "data_path", "./data/")
    data = get_data_from_dir(rag_data_path)
    rag = RAG(data, modele_path=args.rag_path)

    #rag = RAG(data)
    #rag = None
    app.run(host="0.0.0.0", port=5000)
