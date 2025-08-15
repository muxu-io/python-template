"""Simple MQTT client for hello world demo."""

import json
import time
from typing import Optional

import paho.mqtt.client as mqtt


class HelloMqttClient:
    """A simple MQTT client that publishes hello messages."""

    def __init__(self, broker_host: str = "localhost", broker_port: int = 1883):
        """Initialize the MQTT client.
        
        Args:
            broker_host: MQTT broker hostname
            broker_port: MQTT broker port
        """
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.client: Optional[mqtt.Client] = None
        self.connected = False

    def connect(self) -> bool:
        """Connect to the MQTT broker.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.client = mqtt.Client()
            self.client.on_connect = self._on_connect
            self.client.on_disconnect = self._on_disconnect
            
            self.client.connect(self.broker_host, self.broker_port, 60)
            self.client.loop_start()
            
            # Wait for connection
            timeout = 5
            start_time = time.time()
            while not self.connected and (time.time() - start_time) < timeout:
                time.sleep(0.1)
                
            return self.connected
        except Exception as e:
            print(f"Connection failed: {e}")
            return False

    def disconnect(self):
        """Disconnect from the MQTT broker."""
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
            self.connected = False

    def publish_hello(self, name: str = "World") -> bool:
        """Publish a hello message.
        
        Args:
            name: Name to greet
            
        Returns:
            True if message was published successfully
        """
        if not self.connected or not self.client:
            return False
            
        message = {
            "greeting": f"Hello, {name}!",
            "timestamp": time.time()
        }
        
        try:
            result = self.client.publish("hello/greeting", json.dumps(message))
            return result.rc == mqtt.MQTT_ERR_SUCCESS
        except Exception as e:
            print(f"Publish failed: {e}")
            return False

    def _on_connect(self, client, userdata, flags, rc):
        """Callback for when the client connects to the broker."""
        if rc == 0:
            self.connected = True
            print("Connected to MQTT broker")
        else:
            print(f"Failed to connect, return code {rc}")

    def _on_disconnect(self, client, userdata, rc):
        """Callback for when the client disconnects from the broker."""
        self.connected = False
        print("Disconnected from MQTT broker")