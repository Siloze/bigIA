from flask import Flask, render_template, request
import requests

app = Flask(__name__)
API_URL = "http://127.0.0.1:5000/response"
API_CONFIG_URL = "http://127.0.0.1:5000/config"
API_HISTORY_URL = "http://127.0.0.1:5000/history"
    
def send_question(question, pre_prompt, rag_prompt, fichier):
    data = {"question": question, "pre_prompt": pre_prompt, "rag_prompt": rag_prompt}
    files = {}

    if fichier:
        files = {"fichier": (fichier.filename, fichier.stream, fichier.mimetype)}

    response = requests.post(API_URL, data=data, files=files)
    if response.status_code == 200:
        answer = response.json().get("answer", "Aucune réponse.")
    else:
        answer = "Erreur lors de la communication avec l'API."
    return answer

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        question = request.form["question"]
        pre_prompt = request.form.get("pre_prompt", "")
        rag_prompt = request.form.get("rag_prompt", "")
        file = request.files.get("fichier", None)
        answer = send_question(question, pre_prompt, rag_prompt, file)

    return render_template("index.html", history=get_all_history(), preprompt=get_config_param("prompting", "pre_prompt"), ragprompt=get_config_param("prompting", "rag_prompt"))

def get_all_history():
    response = requests.get(API_HISTORY_URL)
    if response.status_code == 200:
        full_history = response.json()
    else:
        full_history = [{"question": "", "answer": "Can't get history from AI deamons. Status code: " + response.status_code}]
    return full_history

def get_config_param(section, key):
    params = {"section": section, "key": key}
    response = requests.get(API_CONFIG_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("value")
    else:
        return "Can't get value from config file: please refresh"  # ou gérer erreur
    
def set_config_param(section, key, value):
    json_data = {"section": section, "key": key, "value": value}
    response = requests.post(API_CONFIG_URL, json=json_data)
    if response.status_code == 200:
        return response.json()
    else:
        return ""  # ou gérer erreur

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
