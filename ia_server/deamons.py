from flask import Flask, request, jsonify
from flask_cors import CORS
import ai
import argparse

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def generate_response():
    prompt = request.args.get("prompt")
    print(prompt)
    if (prompt):
        answer = ai.generate_response(modele, prompt)
        return jsonify({"answer": answer})
    return jsonify({"answer": "Error: prompt is not valid."})

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", type=str, required=True)
    args = parser.parse_args()

    modele = ai.load_modele(args.model_path)
    #modele = None
    app.run(host="0.0.0.0", port=6000)
