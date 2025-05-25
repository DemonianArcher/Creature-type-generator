"""
app.py
------

Flask backend for the Magic: The Gathering Creature Type Generator web application.

This application provides API endpoints to generate random creature types and manage per-user session history.
It is intended to be run behind a WSGI server such as Waitress or Gunicorn.

Endpoints:
    /                - Serves the main web page.
    /api/generate    - GET: Returns a random creature type and updates session history.
    /api/reset       - POST: Clears the session history for the user.

Environment Variables:
    FLASK_SECRET_KEY - Secret key for Flask session management.

Logging:
    Requests and activity are logged to app.log.

Author: Avery Cloutier
Version: 1.0.0
Date: 2025-05-25
"""

import os
from flask import Flask, jsonify, render_template, session, request
from flask_cors import CORS
import random
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
CORS(app, origins=["http://127.0.0.1:8000/"])  # Allows CORS for the specified origin

# Configure logging to work with Flask's logger and rotate logs
log_formatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s')
log_file = 'app.log'
max_bytes = 1 * 1024 * 1024  # 1 MB per log file
backup_count = 3             # Keep up to 3 old log files

file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.INFO)

# Remove default handlers to avoid duplicate logs
if app.logger.hasHandlers():
    app.logger.handlers.clear()
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

# Load creature types once at startup
with open("creature_types.txt", "r", encoding="utf-8") as file:
    creature_types = [line.strip() for line in file if line.strip()]

# Logging to file "app.log"
@app.before_request
def log_request_info():
    app.logger.info(f"{session.get('history', [])} - {request.method} {request.path} from {request.remote_addr}")

# Render the main page via the template in index.html
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint to generate a random creature type
@app.route('/api/generate', methods=['GET'])
def generate_creature():
    if not creature_types:
        return jsonify({"error": "No creature types available."}), 500
    chosen_creature = random.choice(creature_types)
    history = session.get('history', [])
    history.insert(0, chosen_creature)
    session['history'] = history[:50]  # Keep only the last 50
    app.logger.info(f"Generated: {chosen_creature} for {request.remote_addr}")
    return jsonify({"creature_type": chosen_creature, "history": session['history']})

# API endpoint to reset the session history
@app.route('/api/reset', methods=['POST'])
def reset_history():
    session['history'] = []
    app.logger.info(f"History reset by {request.remote_addr}")
    return jsonify({"success": True})

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"Server Error: {error}, Path: {request.path}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run()
