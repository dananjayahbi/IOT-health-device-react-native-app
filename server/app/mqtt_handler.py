# app/mqtt_handler.py
import json
from Adafruit_IO import MQTTClient
from flask import current_app

# Define your Adafruit IO credentials
ADAFRUIT_IO_KEY = 'aio_IGEh551C6e6EleOhzqIpJEcaB9nm'  # Replace with your actual key
ADAFRUIT_IO_USERNAME = 'dananjayahbi'  # Replace with your actual username

# Data storage
data = {
    "steps_count": 0,
    "fall_detected": False
}

# Define callback functions which will be called when certain events happen.
def connected(client):
    """Called when the client connects to Adafruit IO."""
    print('Connected to Adafruit IO! Listening for feed changes...')
    client.subscribe('step-count/json')
    client.subscribe('fall-detection/json')

def disconnected(client):
    """Called when the client disconnects."""
    print('Disconnected from Adafruit IO!')
    client.loop_stop()  # Stop the loop

def message(client, feed_id, payload):
    """Called when a subscribed feed has a new value."""
    print(f'Feed {feed_id} received new value: {payload}')
    payload = json.loads(payload)
    
    if feed_id == 'step-count/json':
        data['steps_count'] = payload['value']
        print(f"Step count updated: {data['steps_count']}")
    elif feed_id == 'fall-detection/json':
        data['fall_detected'] = payload['value'] == "true"
        print(f"Fall detected: {data['fall_detected']}")

def start_mqtt_client():
    """Start the MQTT client."""
    client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
    client.on_connect = connected
    client.on_disconnect = disconnected
    client.on_message = message
    
    client.connect()
    client.loop_background()  # Run the MQTT loop in the background
