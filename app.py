"""This is the flask backend for the web application version of the creature type generator app."""

from flask import Flask, jsonify, render_template
from flask_cors import CORS
import random
import os

app = Flask(__name__)
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
    # Append to generated_creatures.txt
    with open("generated_creatures.txt", "a", encoding="utf-8") as output_file:
        output_file.write(chosen_creature + "\n")
    return jsonify({"creature_type": chosen_creature})

if __name__ == '__main__':
    app.run(debug=True)
