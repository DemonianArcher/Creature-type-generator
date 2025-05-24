"""This is the flask backend for the web application version of the creature type generator app."""

from flask import Flask, jsonify, render_template, session, request
from flask_cors import CORS
import random
import os

app = Flask(__name__)
app.secret_key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIL99D4XPvNOSmAGaOrkkbYJuGvvjzoni+Qg5XxgLHqXA"
CORS(app)

# Load creature types once at startup
with open("creature_types.txt", "r", encoding="utf-8") as file:
    creature_types = [line.strip() for line in file if line.strip()]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['GET'])
def generate_creature():
    if not creature_types:
        return jsonify({"error": "No creature types available."}), 500
    chosen_creature = random.choice(creature_types)
    # Store in session history
    history = session.get('history', [])
    history.insert(0, chosen_creature)
    session['history'] = history
    return jsonify({"creature_type": chosen_creature, "history": history})

@app.route('/api/reset', methods=['POST'])
def reset_history():
    session['history'] = []
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True)
