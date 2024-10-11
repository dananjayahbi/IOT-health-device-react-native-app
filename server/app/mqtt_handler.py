# app/mqtt_handler.py
import json
import logging
from Adafruit_IO import MQTTClient
from .data_handler import read_data, write_data  # Import the new functions

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Define your Adafruit IO credentials
ADAFRUIT_IO_KEY = 'aio_YWsY56ZhamMVPPXIIcsHjfDP7P1F'  # Replace with your actual key
ADAFRUIT_IO_USERNAME = 'dananjayahbi'  # Replace with your actual username

def connected(client):
    """Called when the client connects to Adafruit IO."""
    print('Connected to Adafruit IO! Listening for feed changes...')
    client.subscribe('step-count/json')
    client.subscribe('fall-detection/json')

def disconnected(client):
    """Called when the client disconnects."""
    print('Disconnected from Adafruit IO!')

def message(client, feed_id, payload):
    """Called when a subscribed feed has a new value."""
    payload = json.loads(payload)
    
    # Print the entire payload for debugging
    # print("Received payload:", payload)

    # Print the last value received
    last_value = payload.get('last_value', 'N/A')
    # print(f"New value: {last_value}")

    # Extract values based on feed_id
    if feed_id == 'step-count':
        try:
            steps_count = int(last_value)  # Convert to integer directly from last_value
            print(f"Step count updated: {steps_count}")

            # Write the updated step count and read fall detection status
            data = read_data()  # Read current data
            write_data(steps_count, data['fall_detected'])  # Write updated step count
        except ValueError:
            print(f"Error converting last_value to int: {last_value}")

    elif feed_id == 'fall-detection':
        fall_detected = last_value == "Fall Detected"
        print(f"Fall detected: {fall_detected}")

        # Write the updated fall detection status and read step count
        data = read_data()  # Read current data
        write_data(data['steps_count'], fall_detected)  # Write updated fall detection status


def start_mqtt_client():
    """Start the MQTT client."""
    client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
    client.on_connect = connected
    client.on_disconnect = disconnected
    client.on_message = message
    
    client.connect()
    client.loop_background()  # Run the MQTT loop in the background