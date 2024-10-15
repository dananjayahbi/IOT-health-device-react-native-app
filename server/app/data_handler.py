# app/data_handler.py
import json
import os
import logging

# Configure logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

DATA_FILE = 'app/data.json'  # Path to the data.json file

def ensure_file_exists():
    """Ensure the JSON file exists; if not, create it with default values."""
    if not os.path.exists(DATA_FILE):
        logging.info(f"{DATA_FILE} does not exist. Creating a new file with default values.")
        default_data = {
            "steps_count": 0,
            "fall_detected": {
                "status": False,
                "detected_time": {
                    "date": None,
                    "time": None
                }
            }
        }
        write_data(default_data["steps_count"], default_data["fall_detected"])  # Create file with default values

def read_data():
    """Read data from the JSON file."""
    ensure_file_exists()  # Ensure the file exists before reading
    
    try:
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
            # logging.info(f"Data read successfully: {data}")
            return data
    except Exception as e:
        logging.error(f"Error reading data from {DATA_FILE}: {e}")
        return {
            "steps_count": 0,
            "fall_detected": {
                "status": False,
                "detected_time": {
                    "date": None,
                    "time": None
                }
            }
        }  # Return default data in case of error

def write_data(steps_count, fall_detected):
    """Write data to the JSON file."""
    data = {
        "steps_count": steps_count,
        "fall_detected": fall_detected  # Accept the entire fall_detected object
    }

    try:
        with open(DATA_FILE, 'w') as file:
            json.dump(data, file, indent=4)  # Directly write the data
            # logging.info(f"Data written successfully to {DATA_FILE}: {data}")
    except Exception as e:
        logging.error(f"Error writing data to {DATA_FILE}: {e}")
