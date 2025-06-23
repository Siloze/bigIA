from flask import Flask, render_template, request
import requests

app = Flask(__name__)
API_URL = "http://192.168.1.177:5000/response"  # URL de ton API IA

def write_interaction(question, anwser):
    lignes = [
    "----\n",
    question + "\n",
    "----\n",
    anwser + "\n"
    ]
    with open("history.txt", "a", encoding="utf-8") as f:
        f.write(lignes)

history = []


@app.route("/", methods=["GET", "POST"])
def index():
    print("Méthode :", request.method)  # Pour vérifier que tu rentres bien ici
    answer = ""
    if request.method == "POST":
        question = request.form["question"]
        pre_prompt = request.form.get("pre_prompt", "")  # 👈 récupération ici
        print(pre_prompt)
        response = requests.post(API_URL, json={"question": question, "pre_prompt": pre_prompt})
        if response.status_code == 200:
            answer = response.json().get("answer")
        else:
            answer = "Erreur lors de la communication avec l'API."
        history.append({"question": question, "answer": answer})
    return render_template("index.html", history=history)

if __name__ == "__main__":
    app.run(port=8000)
