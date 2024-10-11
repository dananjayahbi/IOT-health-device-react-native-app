# app/__init__.py
from flask import Flask
from .mqtt_handler import start_mqtt_client  # Import the MQTT client

def create_app():
    app = Flask(__name__)

    # Initialize the MQTT client
    start_mqtt_client()

    from .routes import api  # Import the routes
    app.register_blueprint(api)

    return app
