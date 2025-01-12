# Session 4: Unified Publisher with LoRa, MQTT, and HTTP Interface

This project implements a Unified Publisher that integrates LoRa communication, MQTT message publishing, and an HTTP server interface. It is designed to be a versatile IoT framework that supports message transmission across multiple protocols and includes an interactive control panel for LED and messaging.

## Features

1. **WiFi Connectivity**: Connects to a specified WiFi network.
2. **LoRa Communication**: Transmits messages over LoRa using the `SX127x` module.
3. **MQTT Integration**: Publishes messages to an MQTT broker.
4. **HTTP Interface**: Hosts an HTTP server to control LEDs and send messages via different protocols.
5. **Button Press Handling**: Detects button presses and publishes messages to all supported channels.
6. **LED Control**: Allows control of an onboard LED via HTTP or button press.

---

## File Descriptions

### 1. **`main.py`**
- **Purpose**: Implements the core logic for the Unified Publisher.
- **Key Components**:
  - `UnifiedPublisher` class:
    - **WiFi Connection**: Connects to a predefined WiFi network.
    - **LoRa Initialization**: Configures and uses the `SX127x` LoRa module.
    - **MQTT Client**: Connects to an MQTT broker and publishes messages.
    - **HTTP Server**: Hosts a web interface for controlling the system.
    - **Button Handling**: Toggles an LED and publishes messages on button press.
    - **Concurrency**: Uses `uasyncio` to manage tasks concurrently.
  - `main()` function: Starts the Unified Publisher.

### 2. **`sx127x.py`**
- **Purpose**: Provides a driver for the `SX127x` LoRa module.
- **Key Features**:
  - SPI communication with the LoRa chip.
  - Configurable parameters such as frequency, bandwidth, spreading factor, and coding rate.
  - Methods for sending and receiving messages.
  - Low-level register access for advanced configurations.

### 3. **`umqttsimple.py`**
- **Purpose**: Implements a lightweight MQTT client for message publishing and subscribing.
- **Key Features**:
  - Connection management with MQTT brokers.
  - Message publishing with configurable QoS levels.
  - Subscription support with callbacks for incoming messages.

---

## How to Use

1. **Setup Requirements**:
   - Install the necessary MicroPython libraries.
   - Ensure the hardware setup includes an ESP32/ESP8266 board, an SX127x LoRa module, and a button.

2. **Configuration**:
   - Update `WIFI_SSID` and `WIFI_PASSWORD` in `main.py` with your WiFi credentials.
   - Configure the MQTT broker details (`MQTT_SERVER`, `MQTT_USER`, and `MQTT_PASSWORD`).
   - Adjust LoRa parameters in `LORA_CONFIG` and `LORA_PARAMETERS` if needed.

3. **Deploy**:
   - Flash the `.py` files to your MicroPython-compatible device.
   - Run `main.py` to start the system.

4. **Usage**:
   - Access the HTTP interface at `http://<DEVICE_IP>` to control the LED or publish messages.
   - Use an MQTT client to observe messages on the configured topic.

---

## Dependencies

- **MicroPython**: Ensure your board is running MicroPython.
- **SX127x LoRa Module**: Required for LoRa communication.
- **MQTT Broker**: Required for message publishing over MQTT.

---

## Example HTTP Interface

When accessing the HTTP server, you can:
- Toggle the LED state.
- Publish messages to all protocols, LoRa only, or MQTT only.

---
