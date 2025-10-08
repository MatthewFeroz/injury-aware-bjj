from flask import Flask, request, render_template, jsonify
import os
import json
import re
from ai_service import BJJAIAdvisor
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the JSON file
json_path = os.path.join(current_dir, "bjj_moves.json")

# Load the BJJ knowledge base
with open(json_path, "r") as f:
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

@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "").strip()
    session_id = data.get("session_id", "default")

    if not user_message:
        return jsonify({"error": "message is required"}), 400

    # Minimal in-memory chat history per session
    if not hasattr(app, "_chat_histories"):
        app._chat_histories = {}
    history = app._chat_histories.get(session_id, [])

    # System prompt to guide tone and role
    if not history:
        history.append({
            "role": "system",
            "content": (
                "You are an empathetic BJJ coach and licensed PT. Be concise, practical, and safe. "
                "If user mentions injuries, emphasize modifications and red flags. "
                "CRITICAL: Provide direct, actionable advice only. NO internal reasoning, thinking, or analysis. "
                "NO phrases like 'Let me', 'I'll', 'Based on', 'To answer'. Start immediately with your response."
            ),
        })

    # Append user message
    history.append({"role": "user", "content": user_message})

    # Trim history to last ~10 turns to keep payload small
    trimmed = history[-21:]

    # Call AI
    ai_text = ai_advisor.chat_completion(trimmed, max_tokens=400, temperature=0.1)

    # Append assistant reply and persist
    history.append({"role": "assistant", "content": ai_text})
    app._chat_histories[session_id] = history[-50:]

    return jsonify({
        "session_id": session_id,
        "reply": ai_text,
        "history_len": len(app._chat_histories[session_id])
    })

# Vercel serverless function handler
def handler(request):
    return app(request.environ, lambda *args: None)

# Export the handler for Vercel
app = app
