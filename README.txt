Injury-Aware AI Jiu Jitsu Coach

Injury-Aware AI Coaching is an open-source prototype demonstrating how AI can help athletes adapt their training when dealing with injuries. The system filters Brazilian Jiu Jitsu (BJJ) techniques based on a user’s injury and returns moves to avoid and safe alternatives.

Disclaimer: This tool does not provide medical advice. Always consult a healthcare professional.

---

Features
- JSON knowledge base of BJJ techniques tagged with injury risks.
- Flask API to query injuries → safe vs unsafe moves.
- Future scope: integrate with NVIDIA Nemotron via NIM for reasoning and recovery advice.

---

Project Structure

injury-aware-bjj/

├── app.py               # Flask API
├── bjj_moves.json       # Technique KB
├── requirements.txt     # Dependencies
└── README.md            # Documentation

---

Setup & Run
```bash
git clone https://github.com/MatthewFeroz/injury-aware-bjj.git
cd injury-aware-bjj
pip install -r requirements.txt
python app.py

