############### Imports ###############
import socket
from time import sleep

import network
import uasyncio as asyncio
import ubinascii
from sx127x import SX127x
from machine import SPI, Pin
from umqttsimple import MQTTClient

#######################################


####### Unified Publisher Class ######
class UnifiedPublisher:
    """
    This class provides a unified approach to:
    1) Connect to a WiFi network
    2) Publish messages through MQTT
    3) Send messages via LoRa
    4) Provide an HTTP server interface

    It handles:
    - WiFi connectivity (init_wifi)
    - LoRa configuration and message sending (init_lora, send_lora_message)
    - MQTT setup and message publishing (init_mqtt, send_mqtt_message)
    - HTTP server to control LED and publish messages 
      (init_http_server, handle_http_request)
    - Button press detection and message publication on press 
      (check_button, publish_messages)

    Usage:
        publisher = UnifiedPublisher()
        asyncio.run(publisher.run())
    """

    ###### Protocol Configuration ######
    WIFI_SSID = "IOTNET_2.4"
    WIFI_PASSWORD = "10T@ATC_"

    MQTT_SERVER = "172.20.10.2"
    MQTT_USER = "iot"
    MQTT_PASSWORD = "2024"
    MQTT_TOPIC = b"notification"

    LORA_CONFIG = {
        "miso": 19,
        "mosi": 27,
        "ss": 18,
        "sck": 5,
        "dio_0": 23,
        "reset": 9,
    }

    LORA_PARAMETERS = {
        "frequency": 433e6,
        "tx_power_level": 2,
        "signal_bandwidth": 125e3,
        "spreading_factor": 8,
        "coding_rate": 5,
        "preamble_length": 8,
        "implicit_header": False,
        "sync_word": 0x12,
        "enable_CRC": False,
        "invert_IQ": False,
    }

    ###############################

    ###### Class constructor ######
    def __init__(self):
        """
        Initializes the UnifiedPublisher instance:
        - Sets up an LED pin and a button pin.
        - Initializes WiFi connection.
        - Initializes LoRa module.
        - Initializes MQTT client.
        - Creates a lock for button press handling.
        - Sets up the HTTP server socket.
        """
        self.led = Pin(2, Pin.OUT)
        self.button = Pin(36, Pin.IN)

        self.init_wifi()
        self.init_lora()
        self.init_mqtt()

        self.button_lock = asyncio.Lock()
        self.button_lock.acquire()

        self.server_socket = None
        self.init_http_server()

    ###############################

    #### SetUp Wifi connection ####
    def init_wifi(self):
        """
        Activates WiFi in station mode and attempts to connect to the
        specified access point. Waits until the network is connected.
        """
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(self.WIFI_SSID, self.WIFI_PASSWORD)

        while not self.wlan.isconnected():
            print("Connecting to WiFi...")
            sleep(1)

        print("WiFi Connected!")
        print("IP Address:", self.wlan.ifconfig()[0])

    ###############################

    #### SetUp LoRa connection ####
    def init_lora(self):
        """
        Initializes the SPI interface and configures the SX127x LoRa module
        with the predefined pins and parameters.
        """
        device_spi = SPI(
            baudrate=10000000,
            polarity=0,
            phase=0,
            bits=8,
            firstbit=SPI.MSB,
            sck=Pin(self.LORA_CONFIG["sck"], Pin.OUT, Pin.PULL_DOWN),
            mosi=Pin(self.LORA_CONFIG["mosi"], Pin.OUT, Pin.PULL_UP),
            miso=Pin(self.LORA_CONFIG["miso"], Pin.IN, Pin.PULL_UP),
        )

        self.lora = SX127x(
            device_spi, pins=self.LORA_CONFIG,
            parameters=self.LORA_PARAMETERS
        )

    ###############################

    #### SetUp MQTT connection ####
    def init_mqtt(self):
        """
        Initializes the MQTT client using the credentials defined.
        Attempts to connect to the MQTT broker.
        """
        self.client_id = ubinascii.hexlify(machine.unique_id())
        self.mqtt = MQTTClient(
            self.client_id,
            self.MQTT_SERVER,
            user=self.MQTT_USER,
            password=self.MQTT_PASSWORD,
        )
        try:
            self.mqtt.connect()
            print("MQTT Connected!")
        except Exception as e:
            print("MQTT Connection failed:", str(e))

    ###############################

    #### SetUp HTTP Server ####
    def init_http_server(self):
        """
        Creates a socket to listen for HTTP requests on port 80.
        """
        self.server_socket = socket.socket()
        addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
        self.server_socket.bind(addr)
        self.server_socket.listen(1)
        print("HTTP server listening on port 80")

    ###############################

    #### Checks button value and toggle LED status ####
    async def check_button(self):
        """
        Continuously checks if the button is pressed.
        If pressed, toggles the LED state, publishes the
        corresponding message, and releases the button lock.
        """
        while True:
            if self.button.value():
                print("Button pressed!")
                self.led.value(not self.led.value())
                status = "ON" if self.led.value() else "OFF"
                await self.publish_all(f"Button pressed-LED turned {status}")
                self.button_lock.release()
                await asyncio.sleep_ms(250)
            await asyncio.sleep_ms(10)

    ##################################################

    ######## Publish messages on the different channels #########
    async def publish_messages(self):
        """
        Awaits the acquisition of the button lock, then publishes
        a predefined message ("Button pressed") to all protocols.
        """
        while True:
            await self.button_lock.acquire()
            try:
                await self.publish_all("Button pressed")
            except Exception as e:
                print("Error:", str(e))

    ##################################################

    ######## Provides a response for the requested endpoint #########
    async def handle_http_request(self, client, request):
        """
        Handles a single incoming HTTP request.


        :param client: The socket client connected for HTTP
        :param request: The raw HTTP request data
        """
        request_line = request.decode().split("\r\n")[0]
        method, path, _ = request_line.split(" ")

        response_body = ""
        if path == "/":
            response_body = """
            <html>
            <head>
                <title>Unified Publisher Control</title>
                <style>
                    body { font-family: Arial; margin: 20px; }
                    .button { 
                        padding: 10px 20px; 
                        margin: 5px;
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        cursor: pointer;
                    }
                    .button:hover { background-color: #45a049; }
                    #status { margin: 20px 0; }
                </style>
                <script>
                    async function updateStatus() {
                        const response = await fetch('/led/status');
                        const status = await response.text();
                        document.getElementById('status').textContent=status;
                    }
                    
                    async function controlLED(action) {
                        await fetch('/led/' + action);
                        updateStatus();
                    }
                    
                    setInterval(updateStatus, 2000);
                </script>
            </head>
            <body>
                <h1>Unified Publisher Control Panel</h1>
                
                <h2>LED Control</h2>
                <div id="status">Checking LED status...</div>
                <button class="button" onclick="controlLED('on')">
                   Turn LED On
                </button>
                <button class="button" onclick="controlLED('off')">
                   Turn LED Off
                </button>
                
                <h2>Message Publishing</h2>
                <button class="button" onclick="fetch('/publish/all')">
                   Publish to All
                </button>
                <button class="button" onclick="fetch('/publish/lora')">
                   Publish to LoRa
                </button>
                <button class="button" onclick="fetch('/publish/mqtt')">
                   Publish to MQTT
                </button>
            </body>
            </html>
            """

        elif path == "/led/on":
            self.led.on()
            await self.publish_all("LED turned ON")
            response_body = "LED turned on"

        elif path == "/led/off":
            self.led.off()
            await self.publish_all("LED turned OFF")
            response_body = "LED turned off"

        elif path == "/led/status":
            status = "ON" if self.led.value() else "OFF"
            response_body = f"LED is {status}"

        elif path == "/publish/all":
            await self.publish_all("Message from HTTP")
            response_body = "Published to all protocols"

        elif path == "/publish/lora":
            self.send_lora_message("Message from HTTP")
            response_body = "Published to LoRa"

        elif path == "/publish/mqtt":
            self.send_mqtt_message("Message from HTTP")
            response_body = "Published to MQTT"

        else:
            response_body = "404 Not Found"

        response = f"HTTP/1.1 200 OK\r\nContent-Type: 
                     text/html\r\n\r\n{response_body}"
        client.send(response.encode())
        client.close()

    ################################################

    ############ Process Http Requests #############
    async def handle_http(self):
        """
        Continuously accepts incoming connections on the HTTP server socket.
        On each accepted connection, reads the request and delegates handling
        to the handle_http_request method.
        """
        while True:
            try:
                client, addr = self.server_socket.accept()
                print("Client connected from", addr)
                request = client.recv(1024)
                await self.handle_http_request(client, request)
            except Exception as e:
                print("HTTP handler error:", str(e))
            await asyncio.sleep_ms(10)

    ################################################

    ############# Sends LoRa message ###############
    def send_lora_message(self, message):
        """
        Sends a message via the LoRa module.

        :param message: The string message to be sent via LoRa
        """
        try:
            print(f"Sending LoRa message: {message}")
            self.lora.println(message)
        except Exception as e:
            print(f"LoRa send error: {str(e)}")
    
    ################################################

    ############# Sends MQTT message ###############
    def send_mqtt_message(self, message):
        """
        Publishes a message to the MQTT broker.

        :param message: The string message to be published over MQTT
        """
        try:
            print(f"Publishing MQTT message: {message}")
            self.mqtt.publish(self.MQTT_TOPIC, message.encode())
        except Exception as e:
            print(f"MQTT publish error: {str(e)}")
            try:
                self.mqtt.connect()
                self.mqtt.publish(self.MQTT_TOPIC, message.encode())
            except:
                print("MQTT reconnection failed")
     ################################################

    ###### Publish a message in all the channels ######
    async def publish_all(self, message):
        """
        Publishes the same message to both LoRa and MQTT.

        :param message: The string message to be published
        """
        try:
            self.send_lora_message(message)
            self.send_mqtt_message(message)
            print("Published to all protocols:", message)
        except Exception as e:
            print("Error publishing to all:", str(e))


     ################################################

    ###### Function to run the unified publisher ######
    async def run(self):
        """
        Main asynchronous loop that creates tasks for:
        - Button checking
        - Message publishing
        - HTTP handling

        Runs indefinitely, allowing the tasks to operate concurrently.
        """
        asyncio.create_task(self.check_button())
        asyncio.create_task(self.publish_messages())
        asyncio.create_task(self.handle_http())

        while True:
            await asyncio.sleep(1)


     ################################################

#####################################################

###### Main program function ######
def main():
    """
    Entry point for starting the UnifiedPublisher.
    Creates an instance of UnifiedPublisher and runs it using uasyncio.
    """
    publisher = UnifiedPublisher()
    asyncio.run(publisher.run())


if __name__ == "__main__":
    main()

#####################################################

