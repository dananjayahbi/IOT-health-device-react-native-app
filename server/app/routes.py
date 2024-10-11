# app/routes.py
from flask import Blueprint, jsonify
from .data_handler import read_data  # Import the function to read from JSON

api = Blueprint('api', __name__)

@api.route('/api/steps', methods=['GET'])
def get_steps():
    """Get the latest step count."""
    data = read_data()  # Fetch from JSON
    return jsonify({"steps_count": data['steps_count']})

@api.route('/api/fall', methods=['GET'])
def get_fall_detection():
    """Get the latest fall detection status."""
    data = read_data()  # Fetch from JSON
    return jsonify({"fall_detected": data['fall_detected']})
