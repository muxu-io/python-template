"""Tests for hello_mqtt package."""

import json
import os
import time
from unittest.mock import MagicMock, patch

import pytest

from hello_mqtt import HelloMqttClient


class TestHelloMqttClient:
    """Test cases for HelloMqttClient."""

    def test_init(self):
        """Test client initialization."""
        client = HelloMqttClient()
        assert client.broker_host == "localhost"
        assert client.broker_port == 1883
        assert client.client is None
        assert client.connected is False

    def test_init_custom_params(self):
        """Test client initialization with custom parameters."""
        client = HelloMqttClient("test.broker.com", 8883)
        assert client.broker_host == "test.broker.com"
        assert client.broker_port == 8883

    @patch("hello_mqtt.client.mqtt.Client")
    def test_connect_success(self, mock_mqtt_client):
        """Test successful connection."""
        mock_client_instance = MagicMock()
        mock_mqtt_client.return_value = mock_client_instance
        
        client = HelloMqttClient()
        
        # Simulate successful connection
        def mock_connect(*args):
            client._on_connect(None, None, None, 0)
            
        mock_client_instance.connect.side_effect = mock_connect
        
        result = client.connect()
        
        assert result is True
        assert client.connected is True
        mock_client_instance.connect.assert_called_once_with("localhost", 1883, 60)
        mock_client_instance.loop_start.assert_called_once()

    @patch("hello_mqtt.client.mqtt.Client")
    def test_connect_failure(self, mock_mqtt_client):
        """Test connection failure."""
        mock_client_instance = MagicMock()
        mock_mqtt_client.return_value = mock_client_instance
        mock_client_instance.connect.side_effect = Exception("Connection failed")
        
        client = HelloMqttClient()
        result = client.connect()
        
        assert result is False
        assert client.connected is False

    def test_disconnect(self):
        """Test disconnect functionality."""
        client = HelloMqttClient()
        client.client = MagicMock()
        client.connected = True
        
        client.disconnect()
        
        client.client.loop_stop.assert_called_once()
        client.client.disconnect.assert_called_once()
        assert client.connected is False

    def test_publish_hello_not_connected(self):
        """Test publish when not connected."""
        client = HelloMqttClient()
        result = client.publish_hello()
        assert result is False

    def test_publish_hello_success(self):
        """Test successful hello message publish."""
        client = HelloMqttClient()
        client.client = MagicMock()
        client.connected = True
        
        mock_result = MagicMock()
        mock_result.rc = 0  # MQTT_ERR_SUCCESS
        client.client.publish.return_value = mock_result
        
        result = client.publish_hello("Test")
        
        assert result is True
        client.client.publish.assert_called_once()
        
        # Check the published message
        call_args = client.client.publish.call_args
        topic = call_args[0][0]
        message = json.loads(call_args[0][1])
        
        assert topic == "hello/greeting"
        assert message["greeting"] == "Hello, Test!"
        assert "timestamp" in message

    def test_publish_hello_failure(self):
        """Test failed hello message publish."""
        client = HelloMqttClient()
        client.client = MagicMock()
        client.connected = True
        
        mock_result = MagicMock()
        mock_result.rc = 1  # Error code
        client.client.publish.return_value = mock_result
        
        result = client.publish_hello()
        
        assert result is False

    def test_on_connect_success(self):
        """Test on_connect callback with success."""
        client = HelloMqttClient()
        client._on_connect(None, None, None, 0)
        assert client.connected is True

    def test_on_connect_failure(self):
        """Test on_connect callback with failure."""
        client = HelloMqttClient()
        client._on_connect(None, None, None, 1)
        assert client.connected is False

    def test_on_disconnect(self):
        """Test on_disconnect callback."""
        client = HelloMqttClient()
        client.connected = True
        client._on_disconnect(None, None, None)
        assert client.connected is False


@pytest.mark.integration
class TestHelloMqttClientIntegration:
    """Integration tests with real MQTT broker."""

    def test_real_mqtt_connection(self):
        """Test connection to real MQTT broker."""
        # Use environment variables or default to localhost
        broker_host = os.getenv("MQTT_BROKER_HOST", "localhost")
        broker_port = int(os.getenv("MQTT_BROKER_PORT", "1883"))
        
        client = HelloMqttClient(broker_host, broker_port)
        
        try:
            # Test connection
            connected = client.connect()
            assert connected is True
            
            # Test publish
            published = client.publish_hello("Integration Test")
            assert published is True
            
            # Small delay to ensure message is sent
            time.sleep(0.1)
            
        finally:
            client.disconnect()

    @pytest.mark.slow
    def test_multiple_messages(self):
        """Test publishing multiple messages."""
        broker_host = os.getenv("MQTT_BROKER_HOST", "localhost")
        broker_port = int(os.getenv("MQTT_BROKER_PORT", "1883"))
        
        client = HelloMqttClient(broker_host, broker_port)
        
        try:
            assert client.connect() is True
            
            # Publish multiple messages
            for i in range(5):
                result = client.publish_hello(f"Message {i}")
                assert result is True
                time.sleep(0.1)
                
        finally:
            client.disconnect()