#!/usr/bin/env python3
"""Example usage of hello-mqtt package."""

import sys
import time

# Add src to path for local development
sys.path.insert(0, 'src')

try:
    from hello_mqtt import HelloMqttClient
    
    def main():
        """Demonstrate hello-mqtt usage."""
        print("🚀 Hello MQTT Example")
        
        # Create client
        client = HelloMqttClient()
        print(f"📡 Connecting to MQTT broker at {client.broker_host}:{client.broker_port}")
        
        # Try to connect
        if client.connect():
            print("✅ Connected successfully!")
            
            # Publish some messages
            for name in ["World", "MQTT", "Template"]:
                if client.publish_hello(name):
                    print(f"📤 Published hello message for {name}")
                else:
                    print(f"❌ Failed to publish message for {name}")
                time.sleep(1)
                
            print("✅ Example completed successfully!")
        else:
            print("❌ Failed to connect to MQTT broker")
            print("💡 Make sure an MQTT broker is running on localhost:1883")
            print("   You can start one with: docker run -it -p 1883:1883 eclipse-mosquitto")
            
        # Cleanup
        client.disconnect()
        print("👋 Disconnected from broker")

    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Install dependencies with: pip install -r requirements.txt")
    print("💡 Or install in development mode: pip install -e .")