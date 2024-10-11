from flask import Flask
from dotenv import load_dotenv  # Import dotenv
import os
from .mqtt_handler import start_mqtt_client  # Import the MQTT client

load_dotenv()  # Load environment variables from .env

def create_app():
    app = Flask(__name__)

    # Initialize the MQTT client
    start_mqtt_client()

    from .routes import api  # Import the routes
    app.register_blueprint(api)  # Register the Blueprint

    return app