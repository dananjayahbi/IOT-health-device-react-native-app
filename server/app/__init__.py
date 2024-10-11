# app/__init__.py
from flask import Flask, jsonify
from .mqtt_handler import start_mqtt_client, data

def create_app():
    app = Flask(__name__)

    # Start the MQTT client
    start_mqtt_client()

    @app.route('/', methods=['GET'])
    def index():
        return jsonify({"message": "Welcome to the IoT Health Device API!"}), 200

    @app.route('/api/steps', methods=['GET'])
    def get_steps():
        return jsonify({"steps_count": data['steps_count']}), 200

    @app.route('/api/fall', methods=['GET'])
    def get_fall_status():
        return jsonify({"fall_detected": data['fall_detected']}), 200

    return app
