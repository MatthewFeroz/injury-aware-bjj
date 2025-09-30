from flask import Flask, request, render_template, jsonify
import os
import json
import re
from ai_service import BJJAIAdvisor
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Load the BJJ knowledge base
with open("bjj_moves.json", "r") as f:
    technique_db = json.load(f)

# Initialize AI advisor
ai_advisor = BJJAIAdvisor()

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

@app.route("/api/recommendations", methods=["POST"])
def api_recommendations():
    data = request.get_json(silent=True) or {}
    injuries = data.get("injuries", [])
    if not isinstance(injuries, list):
        injuries = [injuries]

    safe_moves, unsafe_moves = filter_moves(injuries, technique_db)

    ai_recommendations = {}
    recovery_advice = ""

    if injuries:
        ai_recommendations = ai_advisor.get_ai_recommendations(injuries, safe_moves, unsafe_moves)
        recovery_advice = ai_advisor.get_recovery_advice(injuries)

    return jsonify({
        "injuries": injuries,
        "safe_moves": safe_moves,
        "unsafe_moves": unsafe_moves,
        "ai_recommendations": ai_recommendations,
        "recovery_advice": recovery_advice
    })

@app.route("/", methods=["GET", "POST"])
def home():
    injuries = []
    safe_moves, unsafe_moves = [], []
    ai_recommendations = {}
    recovery_advice = ""
    
    if request.method == "POST":
        injuries = request.form.getlist("injuries")
        safe_moves, unsafe_moves = filter_moves(injuries, technique_db)
        
        # Get AI recommendations if injuries are selected
        if injuries:
            ai_recommendations = ai_advisor.get_ai_recommendations(injuries, safe_moves, unsafe_moves)
            recovery_advice = ai_advisor.get_recovery_advice(injuries)

    return render_template(
        "index.html",
        injuries=injuries,
        safe_moves=safe_moves,
        unsafe_moves=unsafe_moves,
        ai_recommendations=ai_recommendations,
        recovery_advice=recovery_advice
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    host = os.getenv("HOST", "0.0.0.0")
    app.run(host=host, port=port, debug=True)