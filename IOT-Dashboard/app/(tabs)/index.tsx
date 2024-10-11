import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ActivityIndicator } from 'react-native';
import { startMqttService } from '../../utils/mqttClient';

export default function HomeScreen() {
  const [steps, setSteps] = useState<number>(0);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // Start MQTT Service and listen to step count
  useEffect(() => {
    startMqttService((newSteps: string) => {
      setSteps(parseInt(newSteps, 10));  // Ensure the value is properly parsed as a number
      setIsLoading(false);  // Data has been loaded
    });
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Step Counter</Text>
      {isLoading ? (
        <ActivityIndicator size="large" color="#1E90FF" />
      ) : (
        <Text style={styles.steps}>{steps} steps</Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  steps: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#1E90FF',
  },
});
