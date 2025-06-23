from flask import Flask, render_template, request
import ai
from rag import RAG
import argparse

print("name: ", __name__)
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    print("Méthode :", request.method)  # Pour vérifier que tu rentres bien ici
    reponse = ""
    if request.method == "POST":
        question = request.form["question"]
        reponse = ai.generate_response(question, modele, rag)
    return render_template("index.html", response=reponse)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--modele_path", type=str, required=True)
    parser.add_argument("--rag_path", type=str, default="sentence-transformers/all-MiniLM-L6-v2")
    parser.add_argument("--rag_data", type=str, default="./data/")
    args = parser.parse_args()

    rag = RAG(args.rag_path, args.rag_data)
    modele = ai.load_modele(args.modele_path)

    app.run()
