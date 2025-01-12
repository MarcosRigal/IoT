# Session 3: MQTT Publisher

## Overview
This project consists of two Python scripts designed for lightweight MQTT communication using MicroPython. It includes an MQTT client library (`umqttsimple.py`) and an application script (`publisher.py`) for publishing data to an MQTT broker.

---

## File Descriptions

### `umqttsimple.py`
This script defines an `MQTTClient` class that handles MQTT protocol operations such as connecting, subscribing, publishing, and managing callbacks. It supports:
- Connecting to an MQTT broker with optional SSL and authentication.
- Publishing messages to specified topics.
- Subscribing to topics with callback functionality.
- Managing last will and testament (LWT) for MQTT clients.

#### Key Features:
- Lightweight implementation for MicroPython devices.
- Handles Quality of Service (QoS) levels 0 and 1.
- Customizable client ID, user authentication, and SSL parameters.

---

### `publisher.py`
This script uses the `umqttsimple` library to publish sensor data to an MQTT broker. It is designed for IoT applications and simulates random sensor data for demonstration purposes.

#### Key Features:
1. **Wi-Fi Connection**:
   - Connects to a Wi-Fi network using given SSID and password.
   - Prints connection status and IP configuration.

2. **MQTT Publishing**:
   - Publishes random sensor data, including humidity, temperature, and status, to the MQTT broker.
   - The data is published to the topic `notification`.

3. **Random Data Generation**:
   - Simulates sensor data with random values for humidity (30–90%), temperature (15.0–30.0°C), and status ("OK" or "Error").

4. **Main Loop**:
   - Connects to the MQTT broker.
   - Publishes data every 5 seconds.

#### Configuration:
Update the following fields in `publisher.py` to fit your setup:
- **Wi-Fi credentials**:
  ```python
  ssid = 'Your_SSID'
  password = 'Your_Password'
  ```
- **MQTT broker details**:
  ```python
  mqtt_server = 'Broker_IP_or_Hostname'
  mqtt_user = 'Your_Username'
  mqtt_pass = 'Your_Password'
  ```

---

## Usage Instructions

1. **Setup MicroPython Environment**:
   - Flash MicroPython firmware on your device (e.g., ESP8266, ESP32).

2. **Upload Files**:
   - Upload `umqttsimple.py` and `publisher.py` to your device.

3. **Update Configurations**:
   - Edit `publisher.py` to match your Wi-Fi and MQTT broker settings.

4. **Run the Script**:
   - Execute `publisher.py` on your device.
   - Monitor the console output to verify successful data publishing.

---

## Example Output
```
Connection successful
('192.168.1.100', '255.255.255.0', '192.168.1.1', '8.8.8.8')
Connected to MQTT broker
Published: {"humidity": 56, "status": "OK", "temperature": 22.5}
Published: {"humidity": 74, "status": "Error", "temperature": 19.8}
```

---

## Dependencies
- MicroPython
- Network module (`network`)
- Random data generation (`random`)
- MQTT client (`umqttsimple`)

---

## Notes
- Ensure your MQTT broker is running and reachable by the device.
- Adjust the publishing interval in `publisher.py` (`time.sleep(5)`) as needed.
- For SSL support, ensure the `ussl` module is available on your MicroPython firmware.

---