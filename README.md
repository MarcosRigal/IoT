
# IoT Practices and Implementations

<div align="center">
    <img width="100%" src="https://tektelic.com/wp-content/uploads/38-IoT.svg" alt="IoT Image">
</div>

This repository contains a series of IoT-related practices implemented using MicroPython on ESP32/ESP8266 microcontrollers. Each session focuses on a specific technology or protocol, progressively building a versatile IoT system. Below is an organized overview of the practices and their corresponding functionalities.

---

## Instructions

The practices are organized as follows:

- **P# Folders**: Each folder represents a practice session with a corresponding number.

---

## Practices Overview

### Session 1: LED Control via HTTP with ESP32
- **Objective**: Control an onboard LED via an HTTP server.
- **Features**:
  - Wi-Fi connectivity.
  - HTTP server with `/on` and `/off` endpoints for LED control.
- **Setup**:
  - ESP32 with MicroPython installed.
  - GPIO2 as default LED pin.
- **Details**: [View Session 1 Details](#session-1-led-control-via-http-with-esp32)

---

### Session 2: LoRa Communication System
- **Objective**: Implement a LoRa-based communication system with a sender and receiver.
- **Features**:
  - LoRa message transmission via a button press.
  - LED notification on message reception.
- **Setup**:
  - SX127x LoRa module and ESP32.
  - Pin configuration for SPI and LoRa control.
- **Details**: [View Session 2 Details](#session-2-lora-communication-system)

---

### Session 3: MQTT Publisher
- **Objective**: Publish sensor data to an MQTT broker.
- **Features**:
  - MQTT message publishing with lightweight implementation.
  - Random sensor data simulation.
- **Setup**:
  - MicroPython libraries and Wi-Fi-enabled device.
  - MQTT broker details for communication.
- **Details**: [View Session 3 Details](#session-3-mqtt-publisher)

---

### Session 4: Unified Publisher with LoRa, MQTT, and HTTP Interface
- **Objective**: Create a unified communication framework combining LoRa, MQTT, and HTTP.
- **Features**:
  - Wi-Fi connectivity and HTTP server.
  - LoRa communication via SX127x module.
  - MQTT message publishing and control interface.
- **Setup**:
  - ESP32/ESP8266, LoRa module, and a button for interaction.
  - Adjustable configurations for Wi-Fi, MQTT, and LoRa.
- **Details**: [View Session 4 Details](#session-4-unified-publisher-with-lora-mqtt-and-http-interface)

---

## Key Dependencies
- MicroPython-compatible hardware (ESP32/ESP8266).
- Required libraries:
  - `uasyncio` for asynchronous tasks.
  - `machine` for hardware interactions.
  - `network` for Wi-Fi operations.
- Protocol-specific modules (`sx127x`, `umqttsimple`).

---

## General Notes
- Ensure Wi-Fi credentials and hardware configurations match your setup.
- Verify the compatibility of your MicroPython firmware and hardware.
- Each session includes example outputs and usage instructions.

---