import * as Notifications from 'expo-notifications';
import { Platform } from 'react-native';

// Request Notification Permissions
export async function requestNotificationPermission() {
  let permissionGranted = false;

  // Check and request permissions
  const { status } = await Notifications.requestPermissionsAsync();
  permissionGranted = status === 'granted';

  if (!permissionGranted) {
    alert('Notification permissions not granted!');
  }
}

// Send Notification for Fall Detection
export async function sendFallNotification() {
  await Notifications.scheduleNotificationAsync({
    content: {
      title: "Emergency Fall Detected!",
      body: "A fall has been detected. Please check immediately!",
    },
    trigger: null,  // Immediate notification
  });
}
