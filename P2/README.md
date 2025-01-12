# Session 2: LoRa Communication System

## Overview

This project implements a LoRa (Long Range) communication system using the SX127x LoRa module. It includes both a sender and receiver application, enabling wireless message exchange. The `sender.py` script transmits messages upon a button press, while the `receiver.py` script listens for incoming messages and provides visual feedback using an LED.

---

## Files

### 1. `receiver.py`
This script is responsible for receiving LoRa messages. Key features include:
- **Message Reception**: Asynchronously listens for incoming messages.
- **Visual Notification**: Blinks an LED upon message reception.
- **Hardware Configuration**: Configures SPI and LoRa parameters for seamless operation.

### 2. `sender.py`
This script handles message transmission via LoRa. Key features include:
- **Button Integration**: Sends a predefined message when the button is pressed.
- **Asynchronous Tasks**: Uses asyncio to monitor button presses and manage message sending.
- **Hardware Configuration**: Configures SPI and LoRa parameters for transmitting data.

### 3. `sx127x.py`
This module defines the `SX127x` class for interacting with the SX127x LoRa module. Key functionalities include:
- **LoRa Initialization**: Configures frequency, bandwidth, spreading factor, and other parameters.
- **Message Transmission and Reception**: Provides methods for sending and receiving data.
- **Register Management**: Handles low-level register interactions with the SX127x module.

---

## Hardware Requirements

- SX127x LoRa module
- Microcontroller with support for Python (e.g., ESP32, Raspberry Pi Pico)
- Push Button (for sender)
- LED (for receiver)

### Pin Configuration
- **SPI Pins**:
  - MISO: GPIO19
  - MOSI: GPIO27
  - SCK: GPIO5
  - SS: GPIO18
- **LoRa Control Pins**:
  - DIO0: GPIO23
  - RESET: GPIO9
- **Application-Specific Pins**:
  - Button (Sender): GPIO36
  - LED (Receiver): GPIO32

---

## Getting Started

### Installation
1. Connect the SX127x LoRa module to your microcontroller as per the pin configuration.
2. Upload the scripts (`sender.py`, `receiver.py`, `sx127x.py`) to your microcontroller.

### Usage

#### Sender
1. Run the `sender.py` script.
2. Press the button to send a message.

#### Receiver
1. Run the `receiver.py` script.
2. Observe LED blinks for each received message, with the message content printed to the console.

---

## Configuration

Modify the following parameters in `sender.py` and `receiver.py` for customization:
- **LoRa Parameters**:
  - Frequency, Bandwidth, Spreading Factor, etc.
- **Pin Assignments**:
  - Adjust GPIO pins as per your hardware setup.

---

## Dependencies

- `uasyncio`: For asynchronous tasks
- `machine`: For hardware interactions

Ensure these libraries are available on your microcontroller.