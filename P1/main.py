############### Imports ###############
import socket

import network
import uasyncio as asyncio
from machine import Pin

#######################################

############### LED Setup #############
led = Pin(2, Pin.OUT)

#######################################


########### Wi-Fi Connection ##########
async def connect_wifi():
    """
    Asynchronously connect to the specified Wi-Fi network.

    1) Create a WLAN object in STA (station) mode.
    2) Activate the interface and connect using the provided SSID and password.
    3) Await connection, printing status messages until connected.
    4) Once connected, print success message and the assigned IP address.
    """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("IOTNET_2.4", "10T@ATC_")

    while not wlan.isconnected():
        print("Connecting...")
        await asyncio.sleep(1)

    print("Successfully connected!")
    print("IP Address:", wlan.ifconfig()[0])


#######################################


########## HTTP Request Handler #######
async def handle_request(cl):
    """
    Handle incoming HTTP requests from a client socket.

    1) Receive up to 1024 bytes of the request.
    2) Check if the request asks to turn the LED on or off.
    3) Prepare an HTML response based on the request.
    4) Send the response, then close the client connection.
    """
    request = cl.recv(1024)
    print("Request received:", request)

    response_body = ""

    if b"/on" in request:
        if led.value() == 1:
            response_body = "<html><body><h1>The LED was already on</h1></body></html>"
        else:
            led.on()
            response_body = "<html><body><h1>LED turned on</h1></body></html>"

    elif b"/off" in request:
        if led.value() == 0:
            response_body = "<html><body><h1>The LED was not on</h1></body></html>"
        else:
            led.off()
            response_body = "<html><body><h1>LED turned off</h1></body></html>"

    else:
        response_body = "<html><body><h1>Unrecognized command</h1></body></html>"

    response = (
        "HTTP/1.1 200 OK\r\n" "Content-Type: text/html\r\n" "\r\n" + response_body
    )

    cl.send(response.encode())
    cl.close()


#######################################


########### HTTP Server Setup #########
async def start_server():
    """
    Create and start a simple HTTP server on port 80.

    1) Bind to '0.0.0.0' to listen on all available interfaces on port 80.
    2) Listen for incoming connections.
    3) Accept clients in an infinite loop and handle each request asynchronously.
    """
    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print("HTTP server listening on:", addr)

    while True:
        cl, remote_addr = s.accept()
        print("Client connected from:", remote_addr)

        await handle_request(cl)


#######################################


############ Main Execution ###########
async def main():
    """
    Main asynchronous function to:
    1) Connect to the configured Wi-Fi network.
    2) Start the HTTP server to handle LED on/off requests.
    """
    await connect_wifi()
    await start_server()


#######################################

########### Event Loop Run ############
if __name__ == "__main__":
    asyncio.run(main())

#######################################
