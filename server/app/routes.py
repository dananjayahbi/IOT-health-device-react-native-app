# app/routes.py
from flask import Blueprint, jsonify

from .data_handler import read_data  # Import the function to read from JSON

# Initialize a Blueprint for routes
api = Blueprint('api', __name__)

# A test route
@api.route('/')
def hello():
    return "Hello, World!"

# Route to get the current status including step count and fall detection
@api.route('/api/status', methods=['GET'])
def get_status():
    """Get the current status including step count and fall detection."""
    data = read_data()  # Fetch from JSON
    return jsonify(data), 200  # Return the complete data object with a 200 status

# If you want to include other endpoints, you can add them here
