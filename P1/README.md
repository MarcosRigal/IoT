# Session 1: LED Control via HTTP with ESP32

This project is a Python-based program designed for an ESP32 microcontroller. It allows you to control an onboard LED via an HTTP server over a Wi-Fi connection. Users can send HTTP requests to turn the LED on or off and receive status feedback.

---

## Features

- **Wi-Fi Connection**: Connects to a specified Wi-Fi network for remote control.
- **HTTP Server**: A lightweight HTTP server listens for incoming client requests.
- **LED Control**: Handle `/on` and `/off` commands to toggle the LED state.
- **Feedback Responses**: Provides immediate feedback via an HTML page for user actions.

---

## Requirements

- **Hardware**:
  - ESP32 microcontroller.
  - Onboard or external LED connected to GPIO2 (default configuration).

- **Software**:
  - MicroPython installed on the ESP32.
  - Dependencies:
    - `network`
    - `uasyncio`
    - `machine`

---

## How It Works

1. **Wi-Fi Setup**:
   - The ESP32 connects to a Wi-Fi network using a specified SSID and password.
   - Network details:
     - SSID: `IOTNET_2.4`
     - Password: `10T@ATC_`

2. **HTTP Server**:
   - Listens on port `80`.
   - Responds to the following requests:
     - `/on`: Turns the LED on.
     - `/off`: Turns the LED off.
     - Other paths: Returns an "Unrecognized command" response.

3. **LED Behavior**:
   - LED toggles state based on the received HTTP command.
   - Maintains state awareness to prevent redundant operations.

---

## Usage

1. **Setup the ESP32**:
   - Flash the MicroPython firmware onto your ESP32.
   - Upload this Python script to the ESP32.

2. **Run the Program**:
   - Power on the ESP32 and it will automatically connect to the configured Wi-Fi.
   - The HTTP server starts and listens for incoming requests.

3. **Control the LED**:
   - Open a web browser or use a tool like `curl` to send HTTP requests:
     - To turn on the LED:
       ```
       http://<ESP32-IP>/on
       ```
     - To turn off the LED:
       ```
       http://<ESP32-IP>/off
       ```
   - Replace `<ESP32-IP>` with the actual IP address assigned to your ESP32 (displayed on successful connection).

---

## Code Structure

1. **Imports**:
   - Includes necessary modules for networking, async operations, and GPIO control.

2. **LED Setup**:
   - Configures GPIO2 as an output pin for LED control.

3. **Wi-Fi Connection**:
   - Implements an asynchronous function to establish a Wi-Fi connection.

4. **HTTP Request Handler**:
   - Parses incoming HTTP requests and controls the LED accordingly.

5. **HTTP Server**:
   - Listens for and handles client connections asynchronously.

6. **Main Function**:
   - Coordinates the Wi-Fi connection and server startup.

7. **Event Loop**:
   - Runs the main asynchronous function.

---

## Customization

- **Wi-Fi Credentials**:
  Modify the `connect_wifi` function to use your own Wi-Fi SSID and password.

- **LED Pin**:
  Update the `Pin` configuration if your LED is connected to a different GPIO pin.

---

## Notes

- Ensure the ESP32 is within the Wi-Fi network range.
- Use appropriate tools to send HTTP requests (e.g., browsers, `curl`, Postman).
- This script is designed for educational and experimental purposes.

---