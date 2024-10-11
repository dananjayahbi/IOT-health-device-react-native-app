# app/mqtt_handler.py
import json
import logging
import os  # Import os to fetch environment variables
from Adafruit_IO import MQTTClient
from .data_handler import read_data, write_data  # Import the new functions
from datetime import datetime
import pytz  # Import pytz for timezone handling
from dotenv import load_dotenv  # Import dotenv

load_dotenv()  # Load environment variables from .env

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Define your Adafruit IO credentials
ADAFRUIT_IO_KEY = os.getenv('ADAFRUIT_IO_KEY')
ADAFRUIT_IO_USERNAME = os.getenv('ADAFRUIT_IO_USERNAME')

# Ensure environment variables are set, otherwise raise an exception
if not ADAFRUIT_IO_KEY or not ADAFRUIT_IO_USERNAME:
    raise EnvironmentError("Please set the ADAFRUIT_IO_KEY and ADAFRUIT_IO_USERNAME environment variables.")

# Define Colombo timezone
COLOMBO_TZ = pytz.timezone('Asia/Colombo')

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
    updated_at = payload.get('updated_at', 'N/A')
    # print(f"New value: {last_value}")
    # print(f"Updated at: {updated_at}")

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

        # Use the updated_at timestamp if fall is detected
        detected_time = None
        if fall_detected:
            # Convert updated_at to Colombo timezone
            utc_time = datetime.strptime(updated_at, '%Y-%m-%d %H:%M:%S %Z')
            utc_time = utc_time.replace(tzinfo=pytz.utc)  # Set UTC timezone
            colombo_time = utc_time.astimezone(COLOMBO_TZ)  # Convert to Colombo timezone
            
            # Extract date and time separately
            date = colombo_time.strftime('%Y-%m-%d')  # Format date
            time = colombo_time.strftime('%H:%M:%S')  # Format time
            detected_time = {"date": date, "time": time}

        print(f"Detected time: {detected_time}")

        # Create the new fall detection structure
        fall_detection_data = {
            "status": fall_detected,
            "detected_time": detected_time
        }

        # Write the updated fall detection status and read step count
        data = read_data()  # Read current data
        write_data(data['steps_count'], fall_detection_data)  # Write updated fall detection status


def start_mqtt_client():
    """Start the MQTT client."""
    client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
    client.on_connect = connected
    client.on_disconnect = disconnected
    client.on_message = message
    
    client.connect()
    client.loop_background()  # Run the MQTT loop in the background