from flask import Flask, request, render_template
import json, re

app = Flask(__name__)

# Load the BJJ knowledge base
with open("bjj_moves.json", "r") as f:
    technique_db = json.load(f)

def normalize_injury(text):
    return re.sub(r"\s+", "_", text.strip().lower())

def filter_moves(injuries, db):
    injury_norms = [normalize_injury(i) for i in injuries]
    safe_moves, unsafe_moves = [], []
    for move in db:
        if any(injury in move["unsafe_for"] for injury in injury_norms):
            unsafe_moves.append(move["technique"])
        else:
            safe_moves.append(move["technique"])
    return safe_moves, unsafe_moves

@app.route("/", methods=["GET", "POST"])
def home():
    injuries = []
    safe_moves, unsafe_moves = [], []
    if request.method == "POST":
        injuries = request.form.getlist("injuries")
        safe_moves, unsafe_moves = filter_moves(injuries, technique_db)

    return render_template(
        "index.html",
        injuries=injuries,
        safe_moves=safe_moves,
        unsafe_moves=unsafe_moves
    )

if __name__ == "__main__":
    app.run(debug=True)