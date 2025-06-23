from flask import Flask, render_template, request
import requests

app = Flask(__name__)
API_URL = "http://127.0.0.1:5000/response"  # URL de ton API IA

@app.route("/", methods=["GET", "POST"])
def index():
    print("Méthode :", request.method)  # Pour vérifier que tu rentres bien ici
    answer = ""
    if request.method == "POST":
        question = request.form["question"]
        response = requests.post(API_URL, json={"question": question})
        if response.status_code == 200:
            answer = response.json().get("answer")
        else:
            answer = "Erreur lors de la communication avec l'API."
    return render_template("index.html", response=answer)

if __name__ == "__main__":
    app.run(port=8000)
