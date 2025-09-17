from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load the BJJ knowledge base at startup
with open("bjj_moves.json", "r") as f:
    technique_db = json.load(f)

def filter_moves(injury, db):
    injury = injury.lower()
    safe_moves = []
    unsafe_moves = []
    for move in db:
        # If injury matches any unsafe_for tag, exclude it
        if any(injury in u for u in move["unsafe_for"]):
            unsafe_moves.append(move["technique"])
        else:
            safe_moves.append(move["technique"])
    return safe_moves, unsafe_moves

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    injury = data.get("injury")

    if not injury:
        return jsonify({"error": "Please provide an injury description"}), 400

    safe_moves, unsafe_moves = filter_moves(injury, technique_db)

    response = {
        "injury": injury,
        "unsafe_moves": unsafe_moves,
        "safe_moves": safe_moves,
        "note": "This is not medical advice. Consult a healthcare professional before training with an injury."
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)