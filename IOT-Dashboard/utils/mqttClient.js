import mqtt from 'mqtt/dist/mqtt';
import { sendFallNotification } from './notifications';

const AIO_USERNAME = 'dananjayahbi';
const AIO_KEY = '';
const STEPS_FEED = `${AIO_USERNAME}/f/step-count`;
const FALL_FEED = `${AIO_USERNAME}/f/fall-detection`;

// Connect to Adafruit IO via WebSocket Secure
const client = mqtt.connect(`wss://io.adafruit.com:443`, {
  username: AIO_USERNAME,
  password: AIO_KEY,
  protocol: 'wss',  // Make sure to use WebSocket Secure (WSS)
  clientId: `mqttjs_${Math.random().toString(16).substr(2, 8)}`,  // Random clientId for uniqueness
});

// Connect to MQTT Feeds
client.on('connect', () => {
  console.log('Connected to MQTT broker');
  client.subscribe(STEPS_FEED, (err) => {
    if (!err) console.log(`Subscribed to ${STEPS_FEED}`);
  });
  client.subscribe(FALL_FEED, (err) => {
    if (!err) console.log(`Subscribed to ${FALL_FEED}`);
  });
});

// Handle Incoming MQTT Messages
client.on('message', (topic, message) => {
  const data = message.toString();

  if (topic === STEPS_FEED) {
    // Handle Step Count Data
    setStepsCount(data);
  } else if (topic === FALL_FEED && data === 'fall_detected') {
    // Handle Fall Detection
    sendFallNotification();
  }
});

// Handle connection errors
client.on('error', (error) => {
  console.error('MQTT connection error:', error);
});

let setStepsCount = () => {};

// This function allows the parent component to update the step count
export const startMqttService = (setStepsCountCallback) => {
  setStepsCount = setStepsCountCallback;
};

export default client;
