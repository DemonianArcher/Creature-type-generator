"""This is the flask backend for the web application version of the creature type generator app."""

import os
from flask import Flask, jsonify, render_template, session, request
from flask_cors import CORS
import random
import logging

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev")
CORS(app, origins=["http://127.0.0.1:8000/"]) # Allows CORS for the specified origin

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# Load creature types once at startup
with open("creature_types.txt", "r", encoding="utf-8") as file:
    creature_types = [line.strip() for line in file if line.strip()]

# Logging to file "app.log"
@app.before_request
def log_request_info():
    logging.info(f"{session.get('history', [])} - {request.method} {request.path} from {request.remote_addr}")

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
    app.run()
